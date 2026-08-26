#!/usr/bin/env python3
"""Fetch, derive, benchmark, validate, and plot comparable country statistics.

Every run is immutable and retains the downloaded source material, normalized
observations, metadata, derived series, peer benchmarks, and figures.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


WB_API = "https://api.worldbank.org/v2"
IMF_API = "https://www.imf.org/external/datamapper/api/v1"
IMF_WEO_SDMX_API = "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.RES/WEO/~/*"
WHO_GHO_API = "https://ghoapi.azureedge.net/api"
ILOSTAT_API = "https://rplumber.ilo.org/data/indicator/"
UNDESA_WPP_CSV = (
    "https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/"
    "CSV_FILES/WPP2024_Demographic_Indicators_Medium.csv.gz"
)
UNDP_HDR_CSV = (
    "https://hdr.undp.org/sites/default/files/2025_HDR/"
    "HDR25_Composite_indices_complete_time_series.csv"
)
WHOGOV_CROSS_SECTIONAL_CSV = (
    "https://www.sv.uio.no/isv/english/research/projects/getgov/"
    "whogov-4.0/whogov_crosssectional_v4.0.csv"
)
SOURCE_LABELS = {
    "world_bank": "World Bank",
    "imf": "International Monetary Fund",
    "imf_weo": "International Monetary Fund",
    "who": "World Health Organization",
    "undp_hdi": "United Nations Development Programme",
    "whogov": "WhoGov (Nuffield College and University of Oslo)",
    "ilostat": "International Labour Organization",
    "undesa_wpp": "United Nations DESA Population Division",
    "unctad": "United Nations Trade and Development",
    "derived": "GDI Country Studies calculation",
    "benchmark": "GDI Country Studies calculation",
}

WHOGOV_VARIABLE_LIMITATIONS = {
    "leaderexperience_continuous": (
        "Counts consecutive years and restarts after removal. It begins at 1 when a leader "
        "first appears, so leaders already in office before 1966 have truncated experience."
    ),
    "leaderexperience_total": (
        "Counts total observed years as leader and begins at 1 on first appearance; experience "
        "before the dataset starts in 1966 is not fully observed."
    ),
    "n_minister": (
        "Counts cabinet ministers only; deputy and junior ministers are excluded. Cabinet "
        "classification is coded manually country by country."
    ),
    "n_core": (
        "Counts manually coded core cabinet positions. It should not be treated as a universal "
        "constitutional category without checking the country coding notes."
    ),
    "n_female_minister": (
        "A count, not a share. Divide by n_minister only for matching country-year observations "
        "and retain missing values when either input is unavailable."
    ),
    "n_female_core": (
        "A count, not a share. Divide by n_core only for matching country-year observations; "
        "the core category is manually coded."
    ),
    "average_minister": (
        "Average time in cabinet among ministers in the annual snapshot. Verify the codebook and "
        "do not interpret tenure alone as expertise or performance."
    ),
    "average_core": (
        "Average time in cabinet among core members in the annual snapshot. Core membership is "
        "manually coded and tenure is not equivalent to administrative capability."
    ),
    "age_minister": (
        "Average age among cabinet ministers with usable birth-year information; inspect "
        "age_share before interpreting changes as changes in cabinet composition."
    ),
    "age_core": (
        "Average age among core cabinet members with usable birth-year information; the core "
        "category is manually coded country by country."
    ),
    "retention_rate_minister": (
        "Share of cabinet ministers also present in the previous annual snapshot. It is affected "
        "by changes in cabinet size and does not directly measure policy continuity."
    ),
    "retention_rateadj_minister": (
        "Previous-year minister retention adjusted for cabinet expansion. It measures personnel "
        "continuity, not administrative performance or policy stability."
    ),
    "retention_rateadj_core": (
        "Previous-year core-member retention adjusted for cabinet expansion. It measures elite "
        "personnel continuity, not administrative performance or policy stability."
    ),
}
_WHOGOV_DOWNLOAD_CACHE: dict[str, tuple[bytes, str]] = {}
_BULK_DOWNLOAD_CACHE: dict[str, tuple[bytes, str]] = {}

REQUIRED_CONFIG_FIELDS = {
    "source",
    "indicator_code",
    "indicator_name",
    "unit",
    "countries",
    "start_year",
    "end_year",
    "value_type",
}


@dataclass
class FetchResult:
    observations: pd.DataFrame
    raw_payload: Any
    endpoint: str
    dataset: str
    source_note: str = ""
    limitations: str = ""
    raw_extension: str = ".json"


def session_with_retries() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=4,
        backoff_factor=0.8,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.headers.update(
        {"Accept": "application/json", "User-Agent": "GDI-country-studies/1.0"}
    )
    return session


def validate_item(item: dict[str, Any], index: int) -> None:
    missing = sorted(REQUIRED_CONFIG_FIELDS - item.keys())
    if missing:
        raise ValueError(f"indicators[{index}] missing fields: {', '.join(missing)}")
    countries = item["countries"]
    if not countries or not isinstance(countries, list):
        raise ValueError(f"indicators[{index}].countries must be a non-empty list")
    if int(item["start_year"]) > int(item["end_year"]):
        raise ValueError(f"indicators[{index}] start_year is after end_year")
    if not str(item["unit"]).strip():
        raise ValueError(f"indicators[{index}] needs an explicit unit")


def base_rows(item: dict[str, Any], frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    for column in (
        "country_code",
        "country_name",
        "year",
        "value",
        "lower_bound",
        "upper_bound",
    ):
        if column not in result.columns:
            result[column] = pd.Series(dtype="object")
    result["source"] = item["source"]
    result["indicator_code"] = item["indicator_code"]
    result["indicator_name"] = item["indicator_name"]
    result["unit"] = item["unit"]
    result["value_type"] = item["value_type"]
    result["frequency"] = item.get("frequency", "annual")
    result["value"] = pd.to_numeric(result["value"], errors="coerce")
    result["lower_bound"] = pd.to_numeric(result["lower_bound"], errors="coerce")
    result["upper_bound"] = pd.to_numeric(result["upper_bound"], errors="coerce")
    result["year"] = pd.to_numeric(result["year"], errors="coerce").astype("Int64")
    result = result.dropna(subset=["year", "value"])
    result["year"] = result["year"].astype(int)
    return result[
        [
            "source",
            "country_code",
            "country_name",
            "year",
            "indicator_code",
            "indicator_name",
            "value",
            "lower_bound",
            "upper_bound",
            "unit",
            "frequency",
            "value_type",
        ]
    ].sort_values(["indicator_code", "country_code", "year"])


def fetch_world_bank(item: dict[str, Any], session: requests.Session) -> FetchResult:
    countries = ";".join(item["countries"])
    code = item["indicator_code"]
    params = {
        "format": "json",
        "date": f"{item['start_year']}:{item['end_year']}",
        "per_page": 20000,
        "source": item.get("source_id", 2),
    }
    endpoint = f"{WB_API}/country/{countries}/indicator/{code}"
    response = session.get(endpoint, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()
    records = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
    rows = [
        {
            "country_code": r.get("countryiso3code"),
            "country_name": (r.get("country") or {}).get("value", ""),
            "year": r.get("date"),
            "value": r.get("value"),
        }
        for r in records
        if r.get("value") is not None
    ]
    metadata_url = f"{WB_API}/indicator/{code}"
    metadata_response = session.get(
        metadata_url,
        params={"format": "json", "source": item.get("source_id", 2)},
        timeout=60,
    )
    metadata_response.raise_for_status()
    metadata_payload = metadata_response.json()
    metadata_records = (
        metadata_payload[1]
        if isinstance(metadata_payload, list) and len(metadata_payload) > 1
        else []
    )
    metadata = metadata_records[0] if metadata_records else {}
    dataset = (metadata.get("source") or {}).get("value", "World Development Indicators")
    return FetchResult(
        base_rows(item, pd.DataFrame(rows)),
        {"data": payload, "indicator_metadata": metadata_payload},
        response.url,
        dataset,
        metadata.get("sourceNote", ""),
    )


def fetch_imf(item: dict[str, Any], session: requests.Session) -> FetchResult:
    code = item["indicator_code"]
    country_path = "/".join(item["countries"])
    years = ",".join(str(y) for y in range(int(item["start_year"]), int(item["end_year"]) + 1))
    endpoint = f"{IMF_API}/{code}/{country_path}"
    response = session.get(endpoint, params={"periods": years}, timeout=60)
    response.raise_for_status()
    payload = response.json()
    block = payload.get("values", {}).get(code, {})
    rows = []
    for country, series in block.items():
        for year, value in series.items():
            if not str(year).isdigit() or value is None:
                continue
            if isinstance(value, list) and len(value) == 1:
                value = value[0]
            rows.append(
                {
                    "country_code": country,
                    "country_name": country,
                    "year": year,
                    "value": value,
                }
            )
    return FetchResult(
        base_rows(item, pd.DataFrame(rows)),
        payload,
        response.url,
        item.get("dataset", "IMF DataMapper"),
        limitations=(
            "DataMapper series may combine historical estimates and projections. "
            "Record the WEO/database vintage and verify the projection boundary before citation."
        ),
    )


def _download_cached(
    endpoint: str,
    session: requests.Session,
    *,
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    timeout: int = 180,
) -> tuple[bytes, str]:
    cache_key = endpoint + "?" + json.dumps(params or {}, sort_keys=True)
    if cache_key in _BULK_DOWNLOAD_CACHE:
        return _BULK_DOWNLOAD_CACHE[cache_key]
    response = session.get(endpoint, headers=headers, params=params, timeout=timeout)
    response.raise_for_status()
    result = (response.content, response.url)
    _BULK_DOWNLOAD_CACHE[cache_key] = result
    return result


def fetch_imf_weo(item: dict[str, Any], session: requests.Session) -> FetchResult:
    """Fetch the official WEO bulk CSV through IMF SDMX 3.0.

    A local CSV/XLSX may be supplied when the IMF edge blocks automated downloads.
    """
    local_file = item.get("local_file")
    endpoint = item.get("endpoint", IMF_WEO_SDMX_API)
    if local_file:
        local_path = Path(local_file).expanduser().resolve()
        raw_bytes = local_path.read_bytes()
        resolved_url = f"local:{local_path}"
        suffix = local_path.suffix.lower()
    else:
        raw_bytes, resolved_url = _download_cached(
            endpoint,
            session,
            headers={"Accept": "text/csv", "User-Agent": "GDI-country-studies/1.0"},
            params={"c[TIME_PERIOD]": f"ge:{int(item['start_year'])}-01"},
        )
        suffix = ".csv"

    from io import BytesIO

    if suffix in {".xlsx", ".xls"}:
        sheet = item.get("sheet_name", "Countries")
        table = pd.read_excel(BytesIO(raw_bytes), sheet_name=sheet)
        country_col = item.get("country_column", "ISO")
        indicator_col = item.get("indicator_column", "WEO Subject Code")
        name_col = item.get("country_name_column", "Country")
        selected = table[
            table[country_col].isin(item["countries"])
            & table[indicator_col].eq(item["indicator_code"])
        ]
        year_columns = [
            c
            for c in selected.columns
            if str(c).isdigit()
            and int(item["start_year"]) <= int(c) <= int(item["end_year"])
        ]
        rows = []
        for _, record in selected.iterrows():
            for year_col in year_columns:
                rows.append(
                    {
                        "country_code": record[country_col],
                        "country_name": record.get(name_col, record[country_col]),
                        "year": int(year_col),
                        "value": record[year_col],
                    }
                )
        raw_extension = suffix
    else:
        table = pd.read_csv(BytesIO(raw_bytes), low_memory=False)
        required = {"COUNTRY", "INDICATOR", "TIME_PERIOD", "OBS_VALUE"}
        missing = sorted(required - set(table.columns))
        if missing:
            raise ValueError(f"IMF WEO bulk CSV missing columns: {', '.join(missing)}")
        selected = table[
            table["COUNTRY"].isin(item["countries"])
            & table["INDICATOR"].eq(item["indicator_code"])
            & pd.to_numeric(table["TIME_PERIOD"], errors="coerce").between(
                int(item["start_year"]), int(item["end_year"])
            )
        ]
        rows = selected.rename(
            columns={"COUNTRY": "country_code", "TIME_PERIOD": "year", "OBS_VALUE": "value"}
        )[["country_code", "year", "value"]]
        rows["country_name"] = rows["country_code"]
        raw_extension = ".csv"

    vintage = item.get("dataset_version", "current WEO SDMX release")
    return FetchResult(
        base_rows(item, pd.DataFrame(rows)),
        raw_bytes,
        resolved_url,
        f"World Economic Outlook, {vintage}",
        limitations=(
            "WEO contains historical data, IMF staff estimates, and projections. Record the "
            "vintage and verify each country's Latest Actual Annual Data before classifying years."
        ),
        raw_extension=raw_extension,
    )


def fetch_who(item: dict[str, Any], session: requests.Session) -> FetchResult:
    code = item["indicator_code"]
    endpoint = f"{WHO_GHO_API}/{code}"
    country_filter = " or ".join(
        f"SpatialDim eq '{country}'" for country in item["countries"]
    )
    filters = item.get("dimensions", {})
    dimension_filter = " and ".join(
        f"{key} eq '{expected}'" for key, expected in filters.items()
    )
    query_filter = f"({country_filter})"
    if dimension_filter:
        query_filter += f" and {dimension_filter}"
    payload_rows: list[dict[str, Any]] = []
    next_url: str | None = endpoint
    first_request = True
    while next_url:
        response = session.get(
            next_url,
            params={"$filter": query_filter} if first_request else None,
            timeout=60,
        )
        response.raise_for_status()
        page = response.json()
        payload_rows.extend(page.get("value", []))
        next_url = page.get("@odata.nextLink")
        first_request = False

    rows = []
    requested = set(item["countries"])
    for record in payload_rows:
        country = record.get("SpatialDim")
        if country not in requested:
            continue
        if any(record.get(key) != expected for key, expected in filters.items()):
            continue
        rows.append(
            {
                "country_code": country,
                "country_name": country,
                "year": record.get("TimeDim"),
                "value": record.get("NumericValue"),
                "lower_bound": record.get("Low"),
                "upper_bound": record.get("High"),
            }
        )
    result = base_rows(item, pd.DataFrame(rows))
    duplicate_keys = result.duplicated(
        ["country_code", "year", "indicator_code"], keep=False
    )
    if duplicate_keys.any():
        raise ValueError(
            f"WHO {code} has multiple observations per country-year. "
            "Add exact Dim1/Dim2/Dim3 filters in the config; no aggregation was performed."
        )
    return FetchResult(
        result,
        payload_rows,
        response.url,
        item.get("dataset", "WHO Global Health Observatory"),
        limitations=(
            "The Colab notebook uses the legacy GHO OData endpoint. WHO announced a migration; "
            "verify the current endpoint and indicator definition before publication."
        ),
    )


def fetch_undp_hdi(item: dict[str, Any], session: requests.Session) -> FetchResult:
    endpoint = item.get("endpoint", UNDP_HDR_CSV)
    response = session.get(endpoint, timeout=90)
    response.raise_for_status()
    raw_bytes = response.content
    from io import BytesIO

    table = pd.read_csv(BytesIO(raw_bytes), encoding="latin-1")
    code = item["indicator_code"].lower()
    countries = set(item["countries"])
    rows = []
    for _, record in table[table["iso3"].isin(countries)].iterrows():
        for column, value in record.items():
            match = re.fullmatch(rf"{re.escape(code)}_(\d{{4}})", str(column).lower())
            if not match:
                continue
            year = int(match.group(1))
            if int(item["start_year"]) <= year <= int(item["end_year"]):
                rows.append(
                    {
                        "country_code": record["iso3"],
                        "country_name": record.get("country", record["iso3"]),
                        "year": year,
                        "value": value,
                    }
                )
    return FetchResult(
        base_rows(item, pd.DataFrame(rows)),
        raw_bytes,
        endpoint,
        item.get("dataset", "UNDP Human Development Report composite indices time series"),
        limitations="The download is vintage-specific; retain the downloaded file and HDR methodology notes.",
        raw_extension=".csv",
    )


def fetch_whogov(item: dict[str, Any], session: requests.Session) -> FetchResult:
    endpoint = item.get("endpoint", WHOGOV_CROSS_SECTIONAL_CSV)
    if endpoint in _WHOGOV_DOWNLOAD_CACHE:
        raw_bytes, resolved_url = _WHOGOV_DOWNLOAD_CACHE[endpoint]
    else:
        response = session.get(
            endpoint,
            headers={
                "Accept": "text/csv,*/*",
                "User-Agent": "Mozilla/5.0 (compatible; GDI Country Studies research client)",
                "Referer": "https://politicscentre.nuffield.ox.ac.uk/whogov-dataset/",
            },
            timeout=120,
        )
        response.raise_for_status()
        raw_bytes = response.content
        resolved_url = response.url
        _WHOGOV_DOWNLOAD_CACHE[endpoint] = (raw_bytes, resolved_url)
    from io import BytesIO

    table = pd.read_csv(BytesIO(raw_bytes))
    required_columns = {"year", "country_isocode", "country_name", item["indicator_code"]}
    missing = sorted(required_columns - set(table.columns))
    if missing:
        raise ValueError(f"WhoGov file missing expected columns: {', '.join(missing)}")
    selected = table[
        table["country_isocode"].isin(item["countries"])
        & table["year"].between(int(item["start_year"]), int(item["end_year"]))
    ]
    rows = selected.rename(
        columns={
            "country_isocode": "country_code",
            "year": "year",
            item["indicator_code"]: "value",
        }
    )[["country_code", "country_name", "year", "value"]]
    version = item.get("dataset_version", "4.0")
    code = item["indicator_code"]
    generic_limit = (
        "WhoGov is a research dataset rather than national official statistics. Annual records "
        "normally represent the cabinet observed in July (September 1966 and January 1970)."
    )
    variable_limit = WHOGOV_VARIABLE_LIMITATIONS.get(code, "Verify the variable in the codebook.")
    if code in {"age_minister", "age_core"} and "age_share" in selected.columns:
        coverage = pd.to_numeric(selected["age_share"], errors="coerce").dropna()
        if not coverage.empty:
            variable_limit += (
                f" Across the selected observations, the share of all cabinet entries with coded "
                f"age ranges from {coverage.min():.3f} to {coverage.max():.3f}."
            )
    return FetchResult(
        base_rows(item, rows),
        raw_bytes,
        resolved_url,
        f"WhoGov cross-sectional dataset, version {version}",
        source_note=(
            "Nyrup, Jacob, and Stuart Bramwell. 2020. Who Governs? A New Global "
            "Dataset on Members of Cabinets. American Political Science Review 114(4): 1366-1374."
        ),
        limitations=f"{generic_limit} {variable_limit}",
        raw_extension=".csv",
    )


def fetch_ilostat(item: dict[str, Any], session: requests.Session) -> FetchResult:
    params: dict[str, Any] = {
        "id": item["indicator_code"],
        "ref_area": "+".join(item["countries"]),
        "timefrom": int(item["start_year"]),
        "timeto": int(item["end_year"]),
        "type": "both",
        "format": ".csv",
    }
    params.update(item.get("filters", {}))
    response = session.get(ILOSTAT_API, params=params, timeout=120)
    response.raise_for_status()
    from io import BytesIO

    table = pd.read_csv(BytesIO(response.content))
    required = {"ref_area", "ref_area.label", "time", "obs_value"}
    missing = sorted(required - set(table.columns))
    if missing:
        raise ValueError(f"ILOSTAT CSV missing columns: {', '.join(missing)}")
    selected = table[table["ref_area"].isin(item["countries"])].copy()
    for column, expected in item.get("filters", {}).items():
        if column not in selected.columns:
            raise ValueError(f"ILOSTAT filter column not returned: {column}")
        values = expected if isinstance(expected, list) else str(expected).split("+")
        selected = selected[selected[column].astype(str).isin([str(value) for value in values])]
    rows = selected.rename(
        columns={
            "ref_area": "country_code",
            "ref_area.label": "country_name",
            "time": "year",
            "obs_value": "value",
        }
    )[["country_code", "country_name", "year", "value"]]
    result = base_rows(item, rows)
    duplicate_keys = result.duplicated(["country_code", "year", "indicator_code"], keep=False)
    if duplicate_keys.any():
        raise ValueError(
            f"ILOSTAT {item['indicator_code']} has multiple sources or classifications per "
            "country-year. Add exact sex/classification/source filters; no averaging was performed."
        )
    indicator_labels = selected.get("indicator.label", pd.Series(dtype=str)).dropna().unique()
    source_labels = selected.get("source.label", pd.Series(dtype=str)).dropna().unique()
    return FetchResult(
        result,
        response.content,
        response.url,
        item.get("dataset", "ILOSTAT indicator web service"),
        source_note=(
            f"Indicator label: {indicator_labels[0] if len(indicator_labels) else item['indicator_name']}; "
            f"underlying sources: {'; '.join(map(str, source_labels[:10]))}"
        ),
        limitations=(
            "ILOSTAT may disseminate national-source observations and ILO modelled estimates. "
            "Preserve source, sex, age, classification, status flags, and methodological notes."
        ),
        raw_extension=".csv",
    )


def fetch_undesa_wpp(item: dict[str, Any], session: requests.Session) -> FetchResult:
    endpoint = item.get("endpoint", UNDESA_WPP_CSV)
    raw_bytes, resolved_url = _download_cached(
        endpoint, session, headers={"User-Agent": "GDI-country-studies/1.0"}
    )
    from io import BytesIO

    table = pd.read_csv(BytesIO(gzip.decompress(raw_bytes)), low_memory=False)
    value_column = item.get("value_column", item["indicator_code"])
    required = {"ISO3_code", "Location", "Variant", "Time", value_column}
    missing = sorted(required - set(table.columns))
    if missing:
        raise ValueError(f"UN DESA WPP CSV missing columns: {', '.join(missing)}")
    variant = item.get("variant", "Medium")
    selected = table[
        table["ISO3_code"].isin(item["countries"])
        & table["Variant"].eq(variant)
        & table["Time"].between(int(item["start_year"]), int(item["end_year"]))
    ]
    rows = selected.rename(
        columns={
            "ISO3_code": "country_code",
            "Location": "country_name",
            "Time": "year",
            value_column: "value",
        }
    )[["country_code", "country_name", "year", "value"]]
    return FetchResult(
        base_rows(item, rows),
        raw_bytes,
        resolved_url,
        item.get("dataset", "World Population Prospects 2024, Medium variant"),
        limitations=(
            "WPP combines estimates and projections. Preserve the revision and projection variant; "
            "population-count columns are generally expressed in thousands unless documented otherwise."
        ),
        raw_extension=".csv.gz",
    )


def fetch_unctad(item: dict[str, Any], session: requests.Session) -> FetchResult:
    endpoint = item.get("endpoint")
    if not endpoint:
        raise ValueError("UNCTAD adapter requires an official table-specific bulk endpoint")
    raw_bytes, resolved_url = _download_cached(
        endpoint,
        session,
        headers={"User-Agent": "Mozilla/5.0", "Referer": "https://unctadstat.unctad.org/"},
    )
    try:
        import py7zr
        import pycountry
    except ImportError as exc:
        raise RuntimeError("UNCTAD bulk extraction requires py7zr and pycountry") from exc

    with tempfile.TemporaryDirectory() as temp_dir:
        from io import BytesIO

        with py7zr.SevenZipFile(BytesIO(raw_bytes), mode="r") as archive:
            archive.extractall(temp_dir)
        csv_files = sorted(Path(temp_dir).rglob("*.csv"))
        if not csv_files:
            raise ValueError("UNCTAD bulk archive contains no CSV file")
        table = pd.read_csv(csv_files[0], low_memory=False)

    value_column = item["value_column"]
    country_column = item.get("country_column", "Economy")
    country_name_column = item.get("country_name_column", "Economy Label")
    year_column = item.get("year_column", "Year")
    required = {country_column, country_name_column, year_column, value_column}
    missing = sorted(required - set(table.columns))
    if missing:
        raise ValueError(f"UNCTAD bulk CSV missing columns: {', '.join(missing)}")
    selected = table.copy()
    for column, expected in item.get("filters", {}).items():
        values = expected if isinstance(expected, list) else [expected]
        selected = selected[selected[column].isin(values)]

    def economy_to_iso3(value: Any) -> str | None:
        if pd.isna(value):
            return None
        text = str(int(value)).zfill(3) if str(value).replace(".0", "").isdigit() else str(value)
        match = pycountry.countries.get(numeric=text)
        return match.alpha_3 if match else None

    selected = selected.assign(country_code=selected[country_column].map(economy_to_iso3))
    selected = selected[selected["country_code"].isin(item["countries"])]
    rows = selected.rename(
        columns={country_name_column: "country_name", year_column: "year", value_column: "value"}
    )[["country_code", "country_name", "year", "value"]]
    result = base_rows(item, rows)
    duplicate_keys = result.duplicated(["country_code", "year", "indicator_code"], keep=False)
    if duplicate_keys.any():
        raise ValueError(
            f"UNCTAD {item['indicator_code']} has multiple rows per country-year. "
            "Add exact dimension filters; no aggregation was performed."
        )
    return FetchResult(
        result,
        raw_bytes,
        resolved_url,
        item.get("dataset", "UNCTAD Data Hub bulk table"),
        limitations=(
            "UNCTAD table dimensions vary. Preserve table ID, release/vintage, economy coding, "
            "flow/product/partner filters, missing-value flags, and footnotes."
        ),
        raw_extension=".7z",
    )


FETCHERS = {
    "world_bank": fetch_world_bank,
    "imf": fetch_imf,
    "imf_weo": fetch_imf_weo,
    "who": fetch_who,
    "undp_hdi": fetch_undp_hdi,
    "whogov": fetch_whogov,
    "ilostat": fetch_ilostat,
    "undesa_wpp": fetch_undesa_wpp,
    "unctad": fetch_unctad,
}


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")


def append_extension(path: Path, extension: str) -> Path:
    """Append, rather than replace, an extension on indicator codes containing dots."""
    return Path(f"{path}.{extension.lstrip('.')}")


def write_raw(path: Path, payload: Any, extension: str) -> Path:
    output_path = append_extension(path, extension)
    if isinstance(payload, bytes):
        output_path.write_bytes(payload)
    else:
        output_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return output_path


def _unique_series(frame: pd.DataFrame, indicator_code: str) -> pd.DataFrame:
    series = frame[frame["indicator_code"].eq(indicator_code)].copy()
    duplicates = series.duplicated(["country_code", "year"], keep=False)
    if duplicates.any():
        raise ValueError(
            f"Indicator {indicator_code} is not unique by country-year; derivation refused"
        )
    return series


def derive_indicators(
    observations: pd.DataFrame, specifications: list[dict[str, Any]]
) -> tuple[list[pd.DataFrame], list[dict[str, Any]]]:
    """Create auditable country-year derived series without imputing missing data."""
    frames: list[pd.DataFrame] = []
    metadata: list[dict[str, Any]] = []
    available = observations.copy()
    for spec in specifications:
        operation = spec["operation"]
        output_code = spec["indicator_code"]
        if operation in {"ratio", "difference", "sum"}:
            left_code = spec["numerator"] if operation == "ratio" else spec["left"]
            right_code = spec["denominator"] if operation == "ratio" else spec["right"]
            left = _unique_series(available, left_code)
            right = _unique_series(available, right_code)
            merged = left.merge(
                right[["country_code", "year", "value"]],
                on=["country_code", "year"],
                how="inner",
                suffixes=("_left", "_right"),
            )
            if operation == "ratio":
                merged = merged[merged["value_right"].ne(0)]
                values = merged["value_left"] / merged["value_right"] * float(spec.get("scale", 1))
                formula = f"({left_code} / {right_code}) * {spec.get('scale', 1)}"
            elif operation == "difference":
                values = merged["value_left"] - merged["value_right"]
                formula = f"{left_code} - {right_code}"
            else:
                values = merged["value_left"] + merged["value_right"]
                formula = f"{left_code} + {right_code}"
            rows = merged[["country_code", "country_name", "year"]].assign(value=values)
        elif operation in {"percent_change", "index_base"}:
            input_code = spec["input_indicator"]
            source = _unique_series(available, input_code).sort_values(["country_code", "year"])
            if operation == "percent_change":
                rows = source[["country_code", "country_name", "year"]].copy()
                rows["value"] = source.groupby("country_code")["value"].pct_change(fill_method=None) * 100
                formula = f"annual percent change in {input_code}"
            else:
                base_year = int(spec["base_year"])
                base = source[source["year"].eq(base_year)][["country_code", "value"]].rename(
                    columns={"value": "base_value"}
                )
                merged = source.merge(base, on="country_code", how="inner")
                merged = merged[merged["base_value"].ne(0)]
                rows = merged[["country_code", "country_name", "year"]].copy()
                rows["value"] = merged["value"] / merged["base_value"] * 100
                formula = f"{input_code}, {base_year}=100"
        else:
            raise ValueError(f"Unsupported derived operation: {operation}")

        item = {
            "source": "derived",
            "indicator_code": output_code,
            "indicator_name": spec["indicator_name"],
            "unit": spec["unit"],
            "value_type": spec.get("value_type", "calculated from cited input series"),
            "frequency": spec.get("frequency", "annual"),
        }
        result = base_rows(item, rows)
        if result.empty:
            raise ValueError(f"Derived indicator {output_code} produced no observations")
        frames.append(result)
        available = pd.concat([available, result], ignore_index=True)
        metadata.append({"spec": spec, "formula": formula})
    return frames, metadata


def build_benchmarks(
    observations: pd.DataFrame, specifications: list[dict[str, Any]]
) -> tuple[list[pd.DataFrame], list[dict[str, Any]]]:
    """Build explicit peer aggregates and optional target-minus-peer gaps."""
    frames: list[pd.DataFrame] = []
    metadata: list[dict[str, Any]] = []
    for spec in specifications:
        input_code = spec["input_indicator"]
        source = _unique_series(observations, input_code)
        peers = list(dict.fromkeys(spec["peer_countries"]))
        statistic = spec.get("statistic", "median")
        if statistic not in {"mean", "median"}:
            raise ValueError("Benchmark statistic must be 'mean' or 'median'")
        peer_rows = source[source["country_code"].isin(peers)]
        grouped = peer_rows.groupby("year")["value"]
        aggregates = (grouped.mean() if statistic == "mean" else grouped.median()).rename("value")
        counts = grouped.count().rename("peer_count")
        aggregate = pd.concat([aggregates, counts], axis=1).reset_index()
        aggregate = aggregate[aggregate["peer_count"].ge(int(spec.get("min_peers", 2)))]
        aggregate["country_code"] = spec.get("benchmark_code", f"PEER_{statistic.upper()}")
        aggregate["country_name"] = spec.get("benchmark_name", f"Peer {statistic}")
        template = source.iloc[0]
        item = {
            "source": "benchmark",
            "indicator_code": spec["indicator_code"],
            "indicator_name": spec["indicator_name"],
            "unit": spec.get("unit", template["unit"]),
            "value_type": spec.get("value_type", "calculated peer-country benchmark"),
            "frequency": spec.get("frequency", template["frequency"]),
        }
        result = base_rows(item, aggregate)
        target = source[source["country_code"].eq(spec["target_country"])].copy()
        if spec.get("include_target", True):
            target = target.assign(
                source="benchmark",
                indicator_code=item["indicator_code"],
                indicator_name=item["indicator_name"],
                unit=item["unit"],
                frequency=item["frequency"],
                value_type=item["value_type"],
            )
            result = pd.concat([target[result.columns], result], ignore_index=True)
        frames.append(result)
        if spec.get("gap_indicator_code"):
            peer_values = aggregate[["year", "value"]].rename(columns={"value": "peer_value"})
            gap = target.merge(peer_values, on="year", how="inner")
            gap["value"] = gap["value"] - gap["peer_value"]
            gap_item = {
                **item,
                "indicator_code": spec["gap_indicator_code"],
                "indicator_name": spec["gap_indicator_name"],
            }
            gap_result = base_rows(gap_item, gap)
            frames.append(gap_result)
        metadata.append(
            {
                "spec": spec,
                "formula": f"{statistic} of {input_code} for {', '.join(peers)}; minimum peers={spec.get('min_peers', 2)}",
            }
        )
    return frames, metadata


def validate_observations(frame: pd.DataFrame) -> list[str]:
    issues = []
    if frame.empty:
        return ["No observations were returned."]
    keys = ["source", "country_code", "year", "indicator_code"]
    duplicate_count = int(frame.duplicated(keys).sum())
    if duplicate_count:
        issues.append(f"{duplicate_count} duplicate observation keys")
    if frame["value"].isna().any():
        issues.append("Missing numeric values remain")
    if frame["unit"].fillna("").str.strip().eq("").any():
        issues.append("At least one observation has no unit")
    return issues


def plot_indicator(frame: pd.DataFrame, output_base: Path, note: str) -> None:
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    for country, group in frame.groupby("country_code"):
        group = group.sort_values("year")
        line = ax.plot(
            group["year"], group["value"], marker="o", linewidth=2, label=country
        )[0]
        if group[["lower_bound", "upper_bound"]].notna().all(axis=1).any():
            bounded = group.dropna(subset=["lower_bound", "upper_bound"])
            ax.fill_between(
                bounded["year"],
                bounded["lower_bound"],
                bounded["upper_bound"],
                color=line.get_color(),
                alpha=0.12,
            )
    name = frame["indicator_name"].iloc[0]
    unit = frame["unit"].iloc[0]
    ax.set_title(name, loc="left", fontsize=14, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel(unit)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(title="Country", frameon=False)
    fig.text(0.01, 0.01, note, fontsize=7.5, color="#444444", wrap=True)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(append_extension(output_base, ".png"), dpi=180, bbox_inches="tight")
    fig.savefig(append_extension(output_base, ".svg"), bbox_inches="tight")
    plt.close(fig)


def run(config_path: Path, country_root: Path, run_id: str | None = None) -> Path:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    indicators = config.get("indicators", [])
    if not indicators:
        raise ValueError("Config must contain a non-empty indicators list")
    for index, item in enumerate(indicators):
        validate_item(item, index)

    run_id = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = country_root / "processed" / "international_statistics" / safe_name(run_id)
    raw_dir = country_root / "raw" / "international_statistics" / safe_name(run_id)
    figure_dir = run_dir / "figures"
    if run_dir.exists() or raw_dir.exists():
        raise FileExistsError(f"Run already exists; choose a new --run-id: {run_id}")
    run_dir.mkdir(parents=True)
    raw_dir.mkdir(parents=True)
    figure_dir.mkdir()

    session = session_with_retries()
    all_frames = []
    metadata_rows = []
    fetch_errors = []
    raw_paths_by_endpoint: dict[tuple[str, str], Path] = {}
    for item in indicators:
        source = item["source"]
        if source not in FETCHERS:
            raise ValueError(f"Unsupported source '{source}'. Supported: {', '.join(FETCHERS)}")
        try:
            result = FETCHERS[source](item, session)
            if result.observations.empty:
                raise ValueError(
                    f"No observations returned for countries {item['countries']}"
                )
        except Exception as exc:
            fetch_errors.append(
                {
                    "source": source,
                    "indicator_code": item["indicator_code"],
                    "error": str(exc),
                }
            )
            continue
        code = item["indicator_code"]
        raw_key = (source, result.endpoint)
        raw_path = raw_paths_by_endpoint.get(raw_key)
        if raw_path is None:
            raw_label = (
                f"v{item.get('dataset_version')}"
                if source == "whogov" and item.get("dataset_version")
                else code
            )
            raw_base = raw_dir / f"{safe_name(source)}__{safe_name(raw_label)}"
            raw_path = write_raw(raw_base, result.raw_payload, result.raw_extension)
            raw_paths_by_endpoint[raw_key] = raw_path
        latest = result.observations.groupby("country_code")["year"].max().to_dict()
        note = (
            f"Source: {SOURCE_LABELS[source]}; dataset: {result.dataset}; indicator: {code}; unit: {item['unit']}; "
            f"countries: {', '.join(item['countries'])}; latest non-missing year: "
            f"{', '.join(f'{k} {v}' for k, v in latest.items())}; processed file: observations.csv."
        )
        plot_indicator(
            result.observations,
            figure_dir / f"{safe_name(source)}__{safe_name(code)}",
            note,
        )
        metadata_rows.append(
            {
                "institution": SOURCE_LABELS[source],
                "dataset": result.dataset,
                "indicator_code": code,
                "indicator_name": item["indicator_name"],
                "country_coverage": ";".join(item["countries"]),
                "unit": item["unit"],
                "frequency": item.get("frequency", "annual"),
                "requested_year_range": f"{item['start_year']}-{item['end_year']}",
                "latest_non_missing_by_country": json.dumps(latest, sort_keys=True),
                "endpoint": result.endpoint,
                "raw_path": str(raw_path.relative_to(country_root)),
                "processed_path": str((run_dir / "observations.csv").relative_to(country_root)),
                "value_type": item["value_type"],
                "transformations": "API/file fields normalized to tidy long format; no interpolation or zero filling",
                "source_note": result.source_note,
                "limitations": "; ".join(
                    x for x in [item.get("limitations", ""), result.limitations] if x
                ),
            }
        )
        all_frames.append(result.observations)

    if not all_frames:
        raise RuntimeError(f"All fetches failed: {fetch_errors}")
    observations = pd.concat(all_frames, ignore_index=True)

    derived_frames, derived_metadata = derive_indicators(
        observations, config.get("derived_indicators", [])
    )
    for frame, detail in zip(derived_frames, derived_metadata, strict=True):
        observations = pd.concat([observations, frame], ignore_index=True)
        spec = detail["spec"]
        code = spec["indicator_code"]
        latest = frame.groupby("country_code")["year"].max().to_dict()
        plot_indicator(
            frame,
            figure_dir / f"derived__{safe_name(code)}",
            f"Source: GDI calculation; formula: {detail['formula']}; inputs retained in observations.csv.",
        )
        metadata_rows.append(
            {
                "institution": SOURCE_LABELS["derived"],
                "dataset": "Derived from normalized input series in this run",
                "indicator_code": code,
                "indicator_name": spec["indicator_name"],
                "country_coverage": ";".join(sorted(frame["country_code"].unique())),
                "unit": spec["unit"],
                "frequency": spec.get("frequency", "annual"),
                "requested_year_range": f"{frame['year'].min()}-{frame['year'].max()}",
                "latest_non_missing_by_country": json.dumps(latest, sort_keys=True),
                "endpoint": "",
                "raw_path": "",
                "processed_path": str((run_dir / "observations.csv").relative_to(country_root)),
                "value_type": spec.get("value_type", "calculated from cited input series"),
                "transformations": detail["formula"],
                "source_note": "Input sources and their metadata remain separate rows in this file.",
                "limitations": spec.get("limitations", "A derived value inherits the definitions, revisions, and missingness of every input series."),
            }
        )

    benchmark_frames, benchmark_metadata = build_benchmarks(
        observations, config.get("benchmarks", [])
    )
    benchmark_index = 0
    for detail in benchmark_metadata:
        spec = detail["spec"]
        item_frames = [benchmark_frames[benchmark_index]]
        benchmark_index += 1
        if spec.get("gap_indicator_code"):
            item_frames.append(benchmark_frames[benchmark_index])
            benchmark_index += 1
        for frame in item_frames:
            observations = pd.concat([observations, frame], ignore_index=True)
            code = frame["indicator_code"].iloc[0]
            name = frame["indicator_name"].iloc[0]
            latest = frame.groupby("country_code")["year"].max().to_dict()
            plot_indicator(
                frame,
                figure_dir / f"benchmark__{safe_name(code)}",
                f"Source: GDI calculation; method: {detail['formula']}; peer list is fixed in the run config.",
            )
            metadata_rows.append(
                {
                    "institution": SOURCE_LABELS["benchmark"],
                    "dataset": "Peer-country benchmark from normalized input series",
                    "indicator_code": code,
                    "indicator_name": name,
                    "country_coverage": ";".join(sorted(frame["country_code"].unique())),
                    "unit": frame["unit"].iloc[0],
                    "frequency": frame["frequency"].iloc[0],
                    "requested_year_range": f"{frame['year'].min()}-{frame['year'].max()}",
                    "latest_non_missing_by_country": json.dumps(latest, sort_keys=True),
                    "endpoint": "",
                    "raw_path": "",
                    "processed_path": str((run_dir / "observations.csv").relative_to(country_root)),
                    "value_type": frame["value_type"].iloc[0],
                    "transformations": detail["formula"],
                    "source_note": f"Target: {spec['target_country']}; peers: {', '.join(spec['peer_countries'])}",
                    "limitations": spec.get("limitations", "Results depend on the theoretically justified peer set, coverage, and aggregation statistic."),
                }
            )
    issues = validate_observations(observations)
    issues.extend(
        f"Fetch failed for {entry['source']}:{entry['indicator_code']}: {entry['error']}"
        for entry in fetch_errors
    )
    observations.to_csv(run_dir / "observations.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame(metadata_rows).to_csv(
        run_dir / "statistical_metadata.csv", index=False, encoding="utf-8-sig"
    )
    manifest = {
        "run_id": run_id,
        "created_at_utc": datetime.now(UTC).isoformat(),
        "config": str(config_path),
        "country_root": str(country_root),
        "rows": len(observations),
        "validation_status": "pass" if not issues else "review",
        "validation_issues": issues,
        "fetch_errors": fetch_errors,
        "warning": "International comparable data do not replace national official data for latest or subnational claims.",
    }
    (run_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return run_dir


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--country-root", type=Path, required=True)
    parser.add_argument("--run-id", help="Optional immutable run directory name")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        output = run(args.config.resolve(), args.country_root.resolve(), args.run_id)
    except Exception as exc:  # CLI boundary: concise error for researchers
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
