import importlib.util
import sys
import unittest
from pathlib import Path

import pandas as pd


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "international_statistics_pipeline.py"
)
SPEC = importlib.util.spec_from_file_location("international_statistics_pipeline", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class InternationalStatisticsPipelineTests(unittest.TestCase):
    def setUp(self):
        self.item = {
            "source": "world_bank",
            "indicator_code": "NY.GDP.MKTP.KD.ZG",
            "indicator_name": "GDP growth",
            "unit": "percent",
            "countries": ["NGA"],
            "start_year": 2020,
            "end_year": 2021,
            "value_type": "international estimate",
        }

    def test_extension_is_appended_to_dotted_indicator_code(self):
        path = Path("world_bank__NY.GDP.MKTP.KD.ZG")
        self.assertEqual(
            MODULE.append_extension(path, ".json").name,
            "world_bank__NY.GDP.MKTP.KD.ZG.json",
        )

    def test_base_rows_keeps_missing_values_missing(self):
        raw = pd.DataFrame(
            [{"country_code": "NGA", "country_name": "Nigeria", "year": 2020, "value": None}]
        )
        result = MODULE.base_rows(self.item, raw)
        self.assertTrue(result.empty)

    def test_duplicate_observation_keys_are_reported(self):
        row = {
            "source": "world_bank",
            "country_code": "NGA",
            "country_name": "Nigeria",
            "year": 2020,
            "indicator_code": "X",
            "indicator_name": "Example",
            "value": 1.0,
            "lower_bound": None,
            "upper_bound": None,
            "unit": "index",
            "frequency": "annual",
            "value_type": "estimate",
        }
        issues = MODULE.validate_observations(pd.DataFrame([row, row]))
        self.assertIn("1 duplicate observation keys", issues)

    def test_whogov_adapter_maps_official_cross_sectional_columns_and_caches(self):
        csv_bytes = (
            "year,country_isocode,country_name,leaderexperience_total,n_minister,age_share\n"
            "2020,NGA,Nigeria,6,24,0.75\n"
            "2021,NGA,Nigeria,7,25,0.80\n"
            "2021,GHA,Ghana,5,19,0.90\n"
        ).encode("utf-8")

        class Response:
            url = "https://example.test/whogov_v4.csv"

            def __init__(self, content):
                self.content = content

            @staticmethod
            def raise_for_status():
                return None

        class Session:
            calls = 0

            def get(self, *args, **kwargs):
                self.calls += 1
                return Response(csv_bytes)

        item = {
            "source": "whogov",
            "dataset_version": "4.0",
            "endpoint": "https://example.test/whogov_v4.csv",
            "indicator_code": "leaderexperience_total",
            "indicator_name": "Leader experience",
            "unit": "years",
            "countries": ["NGA"],
            "start_year": 2020,
            "end_year": 2021,
            "value_type": "research-dataset observation",
        }
        MODULE._WHOGOV_DOWNLOAD_CACHE.clear()
        session = Session()
        first = MODULE.fetch_whogov(item, session)
        second = MODULE.fetch_whogov(item, session)
        self.assertEqual(session.calls, 1)
        self.assertEqual(first.observations["value"].tolist(), [6, 7])
        self.assertEqual(second.dataset, "WhoGov cross-sectional dataset, version 4.0")
        self.assertIn("before the dataset starts in 1966", first.limitations)

    def test_derived_ratio_preserves_only_matched_nonzero_country_years(self):
        rows = []
        for code, values in {"WOMEN": [5, 6], "TOTAL": [20, 0]}.items():
            for year, value in zip([2020, 2021], values):
                item = {**self.item, "indicator_code": code, "indicator_name": code}
                rows.append(
                    MODULE.base_rows(
                        item,
                        pd.DataFrame([{"country_code": "NGA", "country_name": "Nigeria", "year": year, "value": value}]),
                    )
                )
        observations = pd.concat(rows, ignore_index=True)
        frames, metadata = MODULE.derive_indicators(
            observations,
            [{
                "operation": "ratio",
                "numerator": "WOMEN",
                "denominator": "TOTAL",
                "scale": 100,
                "indicator_code": "WOMEN_SHARE",
                "indicator_name": "Women ministers",
                "unit": "percent",
            }],
        )
        self.assertEqual(frames[0]["year"].tolist(), [2020])
        self.assertEqual(frames[0]["value"].tolist(), [25.0])
        self.assertIn("WOMEN / TOTAL", metadata[0]["formula"])

    def test_peer_benchmark_uses_minimum_peer_rule_and_keeps_target(self):
        rows = []
        for country, values in {"NGA": [2, 3], "GHA": [4, 5], "KEN": [6, None]}.items():
            for year, value in zip([2020, 2021], values):
                rows.append({
                    "country_code": country,
                    "country_name": country,
                    "year": year,
                    "value": value,
                })
        source = MODULE.base_rows(self.item, pd.DataFrame(rows))
        frames, _ = MODULE.build_benchmarks(
            source,
            [{
                "input_indicator": self.item["indicator_code"],
                "target_country": "NGA",
                "peer_countries": ["GHA", "KEN"],
                "statistic": "median",
                "min_peers": 2,
                "indicator_code": "GDP_PEERS",
                "indicator_name": "GDP and peer median",
            }],
        )
        result = frames[0]
        peer = result[result["country_code"].eq("PEER_MEDIAN")]
        self.assertEqual(peer["year"].tolist(), [2020])
        self.assertEqual(peer["value"].tolist(), [5.0])
        self.assertEqual(len(result[result["country_code"].eq("NGA")]), 2)

    def test_imf_weo_sdmx_csv_adapter(self):
        csv_bytes = (
            "COUNTRY,INDICATOR,TIME_PERIOD,OBS_VALUE,UNIT\n"
            "NGA,NGDP_RPCH,2020,1.8,Percent change\n"
            "GHA,NGDP_RPCH,2020,0.5,Percent change\n"
        ).encode()

        class Response:
            content = csv_bytes
            url = "https://example.test/weo.csv"
            @staticmethod
            def raise_for_status(): return None

        class Session:
            def get(self, *args, **kwargs): return Response()

        item = {**self.item, "source": "imf_weo", "indicator_code": "NGDP_RPCH"}
        MODULE._BULK_DOWNLOAD_CACHE.clear()
        result = MODULE.fetch_imf_weo(item, Session())
        self.assertEqual(result.observations["value"].tolist(), [1.8])
        self.assertEqual(result.raw_extension, ".csv")

    def test_ilostat_adapter_rejects_unresolved_dimensions(self):
        csv_bytes = (
            "ref_area,ref_area.label,time,obs_value,source,source.label,indicator.label\n"
            "NGA,Nigeria,2020,5,S1,Survey A,Unemployment\n"
            "NGA,Nigeria,2020,6,S2,Survey B,Unemployment\n"
        ).encode()

        class Response:
            content = csv_bytes
            url = "https://example.test/ilo.csv"
            @staticmethod
            def raise_for_status(): return None

        class Session:
            def get(self, *args, **kwargs): return Response()

        item = {**self.item, "source": "ilostat", "indicator_code": "UNE_TEST"}
        with self.assertRaisesRegex(ValueError, "multiple sources"):
            MODULE.fetch_ilostat(item, Session())


if __name__ == "__main__":
    unittest.main()
