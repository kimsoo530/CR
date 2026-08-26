#!/usr/bin/env python3
"""Build a categorized statistical-country-profile appendix from one pipeline run."""

from __future__ import annotations

import argparse
import copy
import csv
import html
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


INK = "#17221f"
MUTED = "#66736e"
BLUE = "#1f5f78"
GOLD = "#c49a3a"
PEER = "#aeb8b4"
GRID = "#dfe5e2"
PEER_COLORS = ["#7f918a", "#c49a3a", "#8b7ea8", "#b56f5d", "#5f8f9d"]
PEER_LINESTYLES = ["--", "-.", ":", (0, (5, 2, 1, 2)), (0, (3, 1))]


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")


def append_extension(path: Path, extension: str) -> Path:
    return Path(f"{path}.{extension.lstrip('.')}")


def format_value(value: float, unit: str) -> str:
    if pd.isna(value):
        return "n/a"
    if "percent" in unit.lower() or "estimate" in unit.lower():
        return f"{value:,.1f}"
    if abs(value) >= 1_000_000:
        return f"{value:,.0f}"
    if abs(value) >= 100:
        return f"{value:,.1f}"
    return f"{value:,.2f}"


def scale_for_plot(frame: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Use reader-facing axis units while retaining raw values in data and tooltips."""
    plotted = frame.copy()
    unit = str(frame["unit"].iloc[0])
    maximum = plotted["value"].abs().max()
    if unit.lower() == "persons" and maximum >= 1_000_000:
        plotted["value"] = plotted["value"] / 1_000_000
        return plotted, "million persons"
    if "current us dollar" in unit.lower() and maximum >= 1_000_000_000:
        plotted["value"] = plotted["value"] / 1_000_000_000
        return plotted, "billion current US dollars"
    return plotted, unit


def chart_subtitle(base: str, spec: dict[str, Any]) -> str:
    note = str(spec.get("subtitle_note", "")).strip()
    return f"{base}; {note}" if note else base


def indicator_frame(observations: pd.DataFrame, code: str) -> pd.DataFrame:
    frame = observations[observations["indicator_code"].eq(code)].copy()
    if frame.empty:
        raise ValueError(f"Indicator not found in observations.csv: {code}")
    duplicates = frame.duplicated(["country_code", "year"], keep=False)
    if duplicates.any():
        raise ValueError(f"Indicator {code} is not unique by country-year")
    return frame.sort_values(["country_code", "year"])


def latest_rows(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.sort_values("year").groupby("country_code", as_index=False).tail(1)


def common_style(ax: plt.Axes, title: str, subtitle: str) -> None:
    ax.set_title(title, loc="left", color=INK, fontsize=14, fontweight="bold", pad=34)
    ax.text(0, 1.015, subtitle, transform=ax.transAxes, color=MUTED, fontsize=9, va="bottom")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8)
    ax.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.8)


def save_figure(fig: plt.Figure, base: Path) -> None:
    fig.savefig(append_extension(base, ".png"), dpi=190, bbox_inches="tight", facecolor="white")
    fig.savefig(append_extension(base, ".svg"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_trend(frame: pd.DataFrame, spec: dict[str, Any], target: str, output: Path) -> str:
    counts = frame.groupby("country_code")["year"].nunique()
    if counts.max() < 8:
        return plot_latest(frame, spec, target, output)
    plotted, unit = scale_for_plot(frame)
    fig, ax = plt.subplots(figsize=(9.6, 5.3))
    peer_index = 0
    for country, group in plotted.groupby("country_code"):
        is_target = country == target
        distinguish_peers = spec.get("distinguish_peers", True)
        if is_target:
            color = BLUE
            linestyle = "-"
        elif distinguish_peers:
            color = PEER_COLORS[peer_index % len(PEER_COLORS)]
            linestyle = PEER_LINESTYLES[peer_index % len(PEER_LINESTYLES)]
            peer_index += 1
        else:
            color = PEER
            linestyle = "--"
        ax.plot(
            group["year"],
            group["value"],
            color=color,
            linewidth=2.8 if is_target else 1.4,
            linestyle=linestyle,
            marker="o" if is_target else None,
            markersize=3.5,
            label=country,
            zorder=3 if is_target else 2,
        )
    common_style(
        ax,
        spec.get("title", frame["indicator_name"].iloc[0]),
        chart_subtitle(f"{unit}; annual observations; focal country highlighted", spec),
    )
    ax.set_ylabel(unit, color=MUTED, fontsize=9)
    ax.set_xlabel("Year", color=MUTED, fontsize=9)
    ax.legend(frameon=False, ncol=min(4, frame["country_code"].nunique()), fontsize=8, loc="upper left")
    fig.tight_layout()
    save_figure(fig, output)
    return "trend"


def plot_latest(frame: pd.DataFrame, spec: dict[str, Any], target: str, output: Path) -> str:
    plotted, unit = scale_for_plot(frame)
    latest = latest_rows(plotted).sort_values("value")
    colors = [BLUE if code == target else PEER for code in latest["country_code"]]
    fig, ax = plt.subplots(figsize=(9.6, 5.1))
    bars = ax.barh(latest["country_code"], latest["value"], color=colors, edgecolor=INK, linewidth=0.4)
    common_style(
        ax,
        spec.get("title", frame["indicator_name"].iloc[0]),
        chart_subtitle(f"Latest non-missing value by country; {unit}; observation years labelled", spec),
    )
    ax.grid(axis="x", color=GRID, linewidth=0.8, alpha=0.8)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel(unit, color=MUTED, fontsize=9)
    if latest["value"].min() >= 0:
        ax.set_xlim(left=0)
    else:
        ax.axvline(0, color=INK, linewidth=0.9)
        span = max(latest["value"].max() - latest["value"].min(), 1)
        ax.set_xlim(latest["value"].min() - span * 0.08, latest["value"].max() + span * 0.18)
    ax.margins(y=0.08)
    for bar, (_, row) in zip(bars, latest.iterrows(), strict=True):
        ax.text(
            row["value"],
            bar.get_y() + bar.get_height() / 2,
            f"  {format_value(row['value'], unit)} ({int(row['year'])})",
            va="center",
            fontsize=8,
            color=INK,
        )
    fig.tight_layout()
    save_figure(fig, output)
    return "latest_bar"


def plot_change(frame: pd.DataFrame, spec: dict[str, Any], target: str, output: Path) -> str:
    plotted, unit = scale_for_plot(frame)
    records = []
    for country, group in plotted.groupby("country_code"):
        ordered = group.sort_values("year")
        if len(ordered) < 2:
            continue
        records.append(
            {
                "country_code": country,
                "value": ordered.iloc[-1]["value"] - ordered.iloc[0]["value"],
                "start": int(ordered.iloc[0]["year"]),
                "end": int(ordered.iloc[-1]["year"]),
            }
        )
    change = pd.DataFrame(records).sort_values("value")
    if change.empty:
        return plot_latest(frame, spec, target, output)
    colors = [BLUE if code == target else (GOLD if value < 0 else PEER) for code, value in zip(change["country_code"], change["value"])]
    fig, ax = plt.subplots(figsize=(9.6, 5.1))
    bars = ax.barh(change["country_code"], change["value"], color=colors, edgecolor=INK, linewidth=0.4)
    common_style(
        ax,
        spec.get("title", frame["indicator_name"].iloc[0]),
        chart_subtitle(f"Latest minus earliest available observation; change in {unit}; periods labelled", spec),
    )
    ax.axvline(0, color=INK, linewidth=0.9)
    ax.grid(axis="x", color=GRID, linewidth=0.8, alpha=0.8)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel(f"Change ({unit})", color=MUTED, fontsize=9)
    span = max(abs(change["value"].min()), abs(change["value"].max()), 1)
    ax.set_xlim(change["value"].min() - span * 0.38, change["value"].max() + span * 0.38)
    for bar, (_, row) in zip(bars, change.iterrows(), strict=True):
        align = "left" if row["value"] >= 0 else "right"
        offset = span * 0.025 if row["value"] >= 0 else -span * 0.025
        ax.text(row["value"] + offset, bar.get_y() + bar.get_height() / 2, f"{row['value']:+.2f} ({row['start']}-{row['end']})", va="center", ha=align, fontsize=8, color=INK)
    fig.tight_layout()
    save_figure(fig, output)
    return "change_bar"


def interactive_payload(frame: pd.DataFrame, chart_type: str, target: str) -> dict[str, Any]:
    unit = str(frame["unit"].iloc[0])
    if chart_type == "latest_bar":
        rows = latest_rows(frame).sort_values("value")
        return {
            "type": chart_type,
            "unit": unit,
            "target": target,
            "rows": [
                {"country": str(row.country_code), "year": int(row.year), "value": float(row.value)}
                for row in rows.itertuples()
            ],
        }
    if chart_type == "change_bar":
        rows = []
        for country, group in frame.groupby("country_code"):
            ordered = group.sort_values("year")
            if len(ordered) < 2:
                continue
            rows.append(
                {
                    "country": str(country),
                    "year_start": int(ordered.iloc[0]["year"]),
                    "year_end": int(ordered.iloc[-1]["year"]),
                    "value_start": float(ordered.iloc[0]["value"]),
                    "value_end": float(ordered.iloc[-1]["value"]),
                    "value": float(ordered.iloc[-1]["value"] - ordered.iloc[0]["value"]),
                }
            )
        return {"type": chart_type, "unit": unit, "target": target, "rows": sorted(rows, key=lambda row: row["value"])}
    points = [
        {"country": str(row.country_code), "year": int(row.year), "value": float(row.value)}
        for row in frame.sort_values(["year", "country_code"]).itertuples()
    ]
    return {
        "type": "trend",
        "unit": unit,
        "target": target,
        "year_min": min(point["year"] for point in points),
        "year_max": max(point["year"] for point in points),
        "points": points,
    }


TOOLTIP_JS = r"""
(() => {
  const node = document.getElementById('chart-data');
  if (!node) return;
  const charts = JSON.parse(node.textContent);
  const number = new Intl.NumberFormat(undefined, {maximumFractionDigits: 2});
  const clamp = (value, low, high) => Math.max(low, Math.min(high, value));
  const show = (box, lines, event) => {
    box.replaceChildren(...lines.map((line, index) => {
      const div = document.createElement('div');
      div.textContent = line.text;
      if (index === 0) div.className = 'tooltip-heading';
      if (line.target) div.classList.add('tooltip-target');
      return div;
    }));
    box.hidden = false;
    const host = box.parentElement.getBoundingClientRect();
    const x = clamp(event.clientX - host.left + 14, 8, Math.max(8, host.width - box.offsetWidth - 8));
    const y = clamp(event.clientY - host.top + 14, 8, Math.max(8, host.height - box.offsetHeight - 8));
    box.style.left = `${x}px`;
    box.style.top = `${y}px`;
  };
  document.querySelectorAll('.interactive-chart').forEach((host) => {
    const payload = charts[host.dataset.chart];
    const box = host.querySelector('.chart-tooltip');
    if (!payload || !box) return;
    const move = (event) => {
      const rect = host.getBoundingClientRect();
      if (payload.type === 'trend') {
        const fraction = clamp((event.clientX - rect.left - rect.width * 0.075) / (rect.width * 0.855), 0, 1);
        const intended = payload.year_min + fraction * (payload.year_max - payload.year_min);
        const years = [...new Set(payload.points.map((point) => point.year))];
        const year = years.reduce((best, candidate) => Math.abs(candidate - intended) < Math.abs(best - intended) ? candidate : best, years[0]);
        const values = payload.points.filter((point) => point.year === year).sort((a, b) => a.country.localeCompare(b.country));
        const lines = [{text: String(year)}].concat(values.map((point) => ({
          text: `${point.country}: ${number.format(point.value)} ${payload.unit}`,
          target: point.country === payload.target
        })));
        show(box, lines, event);
      } else {
        const top = rect.height * 0.14;
        const bottom = rect.height * 0.88;
        const fraction = clamp((event.clientY - rect.top - top) / Math.max(1, bottom - top), 0, 1);
        const index = Math.round((1 - fraction) * (payload.rows.length - 1));
        const row = payload.rows[index];
        if (!row) return;
        const period = payload.type === 'change_bar' ? `${row.year_start}–${row.year_end}` : String(row.year);
        const value = payload.type === 'change_bar' ? `${row.value >= 0 ? '+' : ''}${number.format(row.value)}` : number.format(row.value);
        const lines = [{text: row.country, target: row.country === payload.target}, {text: `${period}: ${value} ${payload.unit}`}];
        if (payload.type === 'change_bar') lines.push({text: `${number.format(row.value_start)} → ${number.format(row.value_end)} ${payload.unit}`});
        show(box, lines, event);
      }
    };
    host.addEventListener('mousemove', move);
    host.addEventListener('mouseleave', () => { box.hidden = true; });
    host.addEventListener('click', move);
  });
})();
"""


def describe_indicator(frame: pd.DataFrame, target: str) -> tuple[str, dict[str, Any]]:
    target_rows = frame[frame["country_code"].eq(target)].sort_values("year")
    if target_rows.empty:
        return f"No observation is available for {target}.", {}
    first = target_rows.iloc[0]
    latest = target_rows.iloc[-1]
    peers = latest_rows(frame[frame["country_code"].ne(target)])
    peer_median = peers["value"].median() if not peers.empty else math.nan
    unit = str(latest["unit"])
    direction = latest["value"] - first["value"]
    text = (
        f"{target} records {format_value(latest['value'], unit)} {unit} in {int(latest['year'])}. "
        f"The earliest available value in this run is {format_value(first['value'], unit)} in {int(first['year'])}, "
        f"a change of {direction:+.2f} {unit}."
    )
    if not pd.isna(peer_median):
        text += f" The median of peers' latest non-missing observations is {format_value(peer_median, unit)} {unit}."
    text += " This is a descriptive comparison; different latest years and source-specific estimation methods require caution."
    return text, {
        "target_latest": latest["value"],
        "target_latest_year": int(latest["year"]),
        "target_first": first["value"],
        "target_first_year": int(first["year"]),
        "change": direction,
        "peer_latest_median": peer_median,
        "unit": unit,
    }


def resolve_config_path(config_path: Path, value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    return path if path.is_absolute() else (config_path.parent / path).resolve()


def load_coverage_catalog(config_path: Path, config: dict[str, Any]) -> pd.DataFrame:
    path = resolve_config_path(config_path, config.get("coverage_catalog"))
    if path is None:
        return pd.DataFrame()
    if not path.exists():
        raise ValueError(f"Coverage catalog not found: {path}")
    return pd.read_csv(path, dtype=str).fillna("")


def expand_categories(
    config: dict[str, Any], observations: pd.DataFrame, metadata: pd.DataFrame, catalog: pd.DataFrame, target: str
) -> list[dict[str, Any]]:
    categories = copy.deepcopy(config["categories"])
    target_codes = set(
        observations.loc[observations["country_code"].eq(target), "indicator_code"].astype(str)
    )
    for category in categories:
        category["indicators"] = [
            spec for spec in category.get("indicators", []) if spec["indicator_code"] in target_codes
        ]
    if not config.get("auto_include_unlisted", False):
        return [category for category in categories if category.get("indicators")]

    listed = {
        spec["indicator_code"]
        for category in categories
        for spec in category.get("indicators", [])
    }
    available = list(dict.fromkeys(observations["indicator_code"].astype(str)))
    catalog_by_code = {}
    if not catalog.empty and "indicator_code" in catalog.columns:
        for _, row in catalog[catalog["indicator_code"].ne("")].iterrows():
            catalog_by_code.setdefault(row["indicator_code"], row.to_dict())

    category_lookup = {category["id"]: category for category in categories}
    for code in available:
        if code in listed or code not in target_codes:
            continue
        row = catalog_by_code.get(code, {})
        category_id = row.get("category_id") or "additional"
        if category_id not in category_lookup:
            category_lookup[category_id] = {
                "id": category_id,
                "title": row.get("category_title") or "Additional available indicators",
                "introduction": "These indicators were present in the validated pipeline run and were added automatically.",
                "indicators": [],
            }
            categories.append(category_lookup[category_id])
        meta = metadata[metadata["indicator_code"].eq(code)]
        obs = observations[observations["indicator_code"].eq(code)]
        fallback_title = str(meta.iloc[0]["indicator_name"]) if not meta.empty and "indicator_name" in meta.columns else str(obs.iloc[0]["indicator_name"])
        category_lookup[category_id]["indicators"].append(
            {
                "indicator_code": code,
                "title": row.get("variable_label") or fallback_title,
                "question": row.get("analytical_question") or "What does this indicator add to the country comparison?",
                "chart_type": row.get("chart_type") or "trend",
            }
        )
    return [category for category in categories if category.get("indicators")]


def coverage_sections(catalog: pd.DataFrame) -> tuple[list[str], str, dict[str, int]]:
    if catalog.empty:
        return [], "", {}
    required = {"domain", "variable_label", "availability", "source_or_adapter", "notes"}
    missing = required.difference(catalog.columns)
    if missing:
        raise ValueError(f"Coverage catalog missing columns: {', '.join(sorted(missing))}")

    counts = catalog["availability"].value_counts().to_dict()
    md = ["", "## Indicator coverage inventory", ""]
    md.append("Reference-notebook variables and core country-profile indicators were classified before charting; a heading is not automatically treated as a comparable statistical variable.")
    md.extend(["", "| Domain | Variable or analysis | Availability | Source / adapter |", "|---|---|---|---|"])
    rows = []
    for _, row in catalog.iterrows():
        md.append(f"| {row['domain']} | {row['variable_label']} | {row['availability']} | {row['source_or_adapter']} |")
        rows.append(
            "<tr>"
            f"<td>{html.escape(row['domain'])}</td>"
            f"<td>{html.escape(row['variable_label'])}</td>"
            f"<td><span class='status'>{html.escape(row['availability'])}</span></td>"
            f"<td>{html.escape(row['source_or_adapter'])}</td>"
            f"<td>{html.escape(row['notes'])}</td>"
            "</tr>"
        )
    summary = ", ".join(f"{key}: {value}" for key, value in sorted(counts.items()))
    section = (
        "<section id='coverage' class='category'><h2>Indicator coverage inventory</h2>"
        "<p>Reference-notebook variables and core country-profile indicators were separated into comparable variables, derived analyses, national-data requirements, and non-variable workflow notes. "
        f"Coverage status — {html.escape(summary)}.</p>"
        "<div class='table-wrap'><table><thead><tr><th>Domain</th><th>Variable or analysis</th><th>Status</th><th>Source / adapter</th><th>Note</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody></table></div></section>"
    )
    return md, section, {str(key): int(value) for key, value in counts.items()}


def audit_required_coverage(
    config: dict[str, Any], target_codes: set[str]
) -> tuple[list[dict[str, Any]], str]:
    """Audit substantive coverage without treating every possible indicator as mandatory."""
    results = []
    for requirement in config.get("required_coverage", []):
        codes = list(dict.fromkeys(str(code) for code in requirement.get("indicator_codes", [])))
        if not codes:
            raise ValueError("Each required_coverage entry must contain indicator_codes")
        minimum = int(requirement.get("minimum_available", len(codes)))
        if minimum < 1 or minimum > len(codes):
            raise ValueError(
                f"required_coverage minimum_available must be between 1 and {len(codes)}"
            )
        available = [code for code in codes if code in target_codes]
        missing = [code for code in codes if code not in target_codes]
        results.append(
            {
                "domain": str(requirement.get("domain", "Unlabelled domain")),
                "minimum_available": minimum,
                "available_count": len(available),
                "available_indicators": available,
                "missing_indicators": missing,
                "status": "pass" if len(available) >= minimum else "review",
                "rationale": str(requirement.get("rationale", "")),
            }
        )
    overall = "pass" if all(row["status"] == "pass" for row in results) else "review"
    return results, overall


def required_coverage_section(
    rows: list[dict[str, Any]], overall: str
) -> tuple[list[str], str]:
    if not rows:
        return [], ""
    md = ["", "## Core coverage audit", ""]
    md.extend(
        [
            f"Overall status: **{overall}**.",
            "",
            "| Domain | Status | Available / minimum | Missing indicators | Rationale |",
            "|---|---|---:|---|---|",
        ]
    )
    html_rows = []
    for row in rows:
        missing = ", ".join(row["missing_indicators"]) or "None"
        count = f"{row['available_count']} / {row['minimum_available']}"
        md.append(
            f"| {row['domain']} | {row['status']} | {count} | {missing} | {row['rationale']} |"
        )
        html_rows.append(
            "<tr>"
            f"<td>{html.escape(row['domain'])}</td>"
            f"<td><span class='status'>{html.escape(row['status'])}</span></td>"
            f"<td>{html.escape(count)}</td>"
            f"<td>{html.escape(missing)}</td>"
            f"<td>{html.escape(row['rationale'])}</td>"
            "</tr>"
        )
    section = (
        "<section id='core-coverage' class='category'><h2>Core coverage audit</h2>"
        f"<p>Overall status: <strong>{html.escape(overall)}</strong>. The threshold is domain-specific so sparse but important series do not silently disappear.</p>"
        "<div class='table-wrap'><table><thead><tr><th>Domain</th><th>Status</th><th>Available / minimum</th><th>Missing indicators</th><th>Rationale</th></tr></thead>"
        f"<tbody>{''.join(html_rows)}</tbody></table></div></section>"
    )
    return md, section


def build(config_path: Path, run_dir: Path, output_dir: Path) -> Path:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    observations = pd.read_csv(run_dir / "observations.csv")
    metadata = pd.read_csv(run_dir / "statistical_metadata.csv").fillna("")
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("validation_status") != "pass":
        raise ValueError("Input pipeline run is not validation_status=pass")

    target = config["country_code"]
    catalog = load_coverage_catalog(config_path, config)
    if not catalog.empty and "indicator_code" in catalog.columns:
        present_codes = set(observations["indicator_code"].astype(str))
        target_codes = set(
            observations.loc[observations["country_code"].eq(target), "indicator_code"].astype(str)
        )
        catalog.loc[catalog["indicator_code"].isin(target_codes), "availability"] = "available_current_run"
        catalog.loc[
            catalog["indicator_code"].isin(present_codes - target_codes), "availability"
        ] = "target_data_unavailable"
    categories = expand_categories(config, observations, metadata, catalog, target)
    target_codes = set(
        observations.loc[observations["country_code"].eq(target), "indicator_code"].astype(str)
    )
    core_rows, core_status = audit_required_coverage(config, target_codes)
    output_dir.mkdir(parents=True, exist_ok=True)
    figure_dir = output_dir / "figures"
    figure_dir.mkdir(exist_ok=True)
    md_lines = [f"# {config.get('title', 'Statistical Country Profile')}", "", config.get("introduction", "")]
    html_sections = []
    chart_rows = []
    summary_rows = []
    chart_payloads = {}

    for category in categories:
        md_lines.extend(["", f"## {category['title']}", "", category.get("introduction", "")])
        cards = []
        for spec in category["indicators"]:
            code = spec["indicator_code"]
            frame = indicator_frame(observations, code)
            base = figure_dir / safe_name(code)
            requested = spec.get("chart_type", "trend")
            if requested == "latest_bar":
                actual = plot_latest(frame, spec, target, base)
            elif requested == "change_bar":
                actual = plot_change(frame, spec, target, base)
            else:
                actual = plot_trend(frame, spec, target, base)
            description, summary = describe_indicator(frame, target)
            chart_payloads[code] = interactive_payload(frame, actual, target)
            meta = metadata[metadata["indicator_code"].eq(code)]
            institution = str(meta.iloc[0]["institution"]) if not meta.empty else str(frame["source"].iloc[0])
            dataset = str(meta.iloc[0]["dataset"]) if not meta.empty else ""
            limitations = str(meta.iloc[0]["limitations"]) if not meta.empty else ""
            note = f"Source: {institution}; {dataset}; indicator {code}; unit: {frame['unit'].iloc[0]}."
            if limitations:
                note += f" Limitation: {limitations}"
            md_lines.extend(
                [
                    "",
                    f"### {spec.get('title', frame['indicator_name'].iloc[0])}",
                    "",
                    description,
                    "",
                    f"![{spec.get('title', code)}](figures/{base.name}.png)",
                    "",
                    note,
                ]
            )
            cards.append(
                f"<section class='chart-card'><h3>{html.escape(spec.get('title', frame['indicator_name'].iloc[0]))}</h3>"
                f"<p>{html.escape(description)}</p><div class='interactive-chart' data-chart='{html.escape(code)}' tabindex='0' aria-label='{html.escape(spec.get('title', code))}; move the pointer over the chart to inspect values'>"
                f"<img src='figures/{html.escape(base.name)}.svg' alt='{html.escape(spec.get('title', code))}'><div class='chart-tooltip' role='status' hidden></div></div>"
                f"<p class='source-note'>{html.escape(note)}</p></section>"
            )
            chart_rows.append(
                {
                    "category": category["id"],
                    "indicator_code": code,
                    "question": spec.get("question", ""),
                    "requested_chart_type": requested,
                    "actual_chart_type": actual,
                    "countries": ";".join(sorted(frame["country_code"].unique())),
                    "year_start": int(frame["year"].min()),
                    "year_end": int(frame["year"].max()),
                    "unit": frame["unit"].iloc[0],
                    "png": f"figures/{base.name}.png",
                    "svg": f"figures/{base.name}.svg",
                }
            )
            summary_rows.append({"category": category["id"], "indicator_code": code, **summary})
        html_sections.append(
            f"<section id='{html.escape(category['id'])}' class='category'><h2>{html.escape(category['title'])}</h2>"
            f"<p>{html.escape(category.get('introduction', ''))}</p>{''.join(cards)}</section>"
        )

    core_md, core_html = required_coverage_section(core_rows, core_status)
    md_lines.extend(core_md)
    coverage_md, coverage_html, coverage_counts = coverage_sections(catalog)
    md_lines.extend(coverage_md)
    (output_dir / "statistical_country_profile.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    pd.DataFrame(summary_rows).to_csv(output_dir / "summary_statistics.csv", index=False, encoding="utf-8-sig")
    with (output_dir / "chart_manifest.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(chart_rows[0]))
        writer.writeheader()
        writer.writerows(chart_rows)

    nav = "".join(f"<a href='#{html.escape(c['id'])}'>{html.escape(c['title'])}</a>" for c in categories)
    if core_html:
        nav += "<a href='#core-coverage'>Core coverage audit</a>"
    if coverage_html:
        nav += "<a href='#coverage'>Variable coverage</a>"
    chart_data_json = (
        json.dumps(chart_payloads, ensure_ascii=False)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )
    book_href = str(config.get("book_home_href", "")).strip()
    book_label = str(config.get("book_home_label", "Back to the country study")).strip()
    book_link = (
        f"<a class='book-return' href='{html.escape(book_href, quote=True)}'>{html.escape(book_label)}</a>"
        if book_href
        else ""
    )
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(config.get('title', 'Statistical Country Profile'))}</title>
<style>
:root{{--ink:{INK};--muted:{MUTED};--line:{GRID};--blue:{BLUE};--paper:#f7f8f6;--panel:#fff}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:Georgia,'Times New Roman',serif;line-height:1.65}}
header{{background:#163c3c;color:#fff;padding:54px max(24px,calc((100vw - 1120px)/2)) 42px}}header p{{max-width:800px;margin:12px 0 0;color:#dce8e4}}.book-return{{display:inline-block;margin-bottom:18px;color:#fff;font:700 13px Arial,sans-serif;text-decoration:none;border:1px solid rgba(255,255,255,.55);border-radius:999px;padding:7px 11px}}.book-return:hover{{background:rgba(255,255,255,.12)}}
main{{max-width:1120px;margin:auto;padding:28px 24px 80px}}nav{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:28px}}nav a{{font:13px Arial,sans-serif;color:var(--blue);background:#fff;border:1px solid var(--line);border-radius:999px;padding:7px 11px;text-decoration:none}}
.category{{padding-top:16px}}h2{{font-size:30px;border-bottom:1px solid var(--line);padding-bottom:9px}}.chart-card{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:22px;margin:22px 0}}.chart-card h3{{font:700 20px Arial,sans-serif;margin-top:0}}.chart-card img{{width:100%;height:auto;display:block;margin:14px 0}}.source-note{{font:12px/1.5 Arial,sans-serif;color:var(--muted)}}
.table-wrap{{overflow-x:auto;background:#fff;border:1px solid var(--line);border-radius:10px}}table{{border-collapse:collapse;width:100%;font:13px/1.45 Arial,sans-serif}}th,td{{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}th{{background:#eef3f0}}.status{{white-space:nowrap;font-weight:700;color:var(--blue)}}
.interactive-chart{{position:relative;cursor:crosshair;outline:none}}.interactive-chart:focus{{box-shadow:0 0 0 3px rgba(31,95,120,.22);border-radius:6px}}.chart-tooltip{{position:absolute;z-index:5;max-width:300px;padding:9px 11px;background:rgba(23,34,31,.94);color:#fff;border-radius:6px;box-shadow:0 5px 18px rgba(0,0,0,.2);font:12px/1.45 Arial,sans-serif;pointer-events:none}}.tooltip-heading{{font-weight:700;border-bottom:1px solid rgba(255,255,255,.25);padding-bottom:3px;margin-bottom:3px}}.tooltip-target{{color:#8fd3ec;font-weight:700}}
@media(max-width:700px){{header{{padding:34px 20px}}main{{padding:20px 14px 60px}}h1{{font-size:34px}}h2{{font-size:25px}}.chart-card{{padding:14px}}}}
</style></head><body><header>{book_link}<h1>{html.escape(config.get('title', 'Statistical Country Profile'))}</h1><p>{html.escape(config.get('introduction', ''))}</p></header><main><nav>{nav}</nav>{''.join(html_sections)}{core_html}{coverage_html}</main><script id='chart-data' type='application/json'>{chart_data_json}</script><script src='chart-tooltips.js' defer></script></body></html>"""
    output = output_dir / "index.html"
    output.write_text(document, encoding="utf-8")
    (output_dir / "chart-tooltips.js").write_text(TOOLTIP_JS.strip() + "\n", encoding="utf-8")
    input_codes = set(observations["indicator_code"].astype(str))
    visualized_codes = {row["indicator_code"] for row in chart_rows}
    validation = {
        "input_run": str(run_dir),
        "input_rows": len(observations),
        "input_validation_status": manifest.get("validation_status"),
        "categories": len(categories),
        "charts": len(chart_rows),
        "input_indicators": len(input_codes),
        "target_available_indicators": len(target_codes),
        "visualized_indicators": len(visualized_codes),
        "target_missing_indicators": sorted(input_codes - target_codes),
        "omitted_input_indicators": sorted(target_codes - visualized_codes),
        "coverage_status_counts": coverage_counts,
        "core_coverage_status": core_status,
        "core_coverage_requirements": core_rows,
        "core_coverage_failed_domains": [
            row["domain"] for row in core_rows if row["status"] != "pass"
        ],
        "missing_images": [row["png"] for row in chart_rows if not (output_dir / row["png"]).exists()],
    }
    (output_dir / "validation.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    return output


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        output = build(args.config.resolve(), args.run_dir.resolve(), args.output_dir.resolve())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
