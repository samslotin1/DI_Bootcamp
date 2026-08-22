"""Clean, transform, integrate, and summarize the Global Terrorism Database.

The pipeline keeps large data files under data/, which is ignored by git.
It creates trackable summary CSV files, SVG charts, and a report.
"""

from __future__ import annotations

import csv
import json
import math
import re
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
EXTRACTED_DIR = DATA_DIR / "extracted"
EXTERNAL_DIR = DATA_DIR / "external"
PROCESSED_DIR = DATA_DIR / "processed"
SUMMARY_DIR = PROJECT_ROOT / "outputs" / "summaries"
FIGURE_DIR = PROJECT_ROOT / "outputs" / "figures"

GTD_URL = (
    "https://github.com/devtlv/Datasets-DA-Bootcamp-2-/raw/refs/heads/main/"
    "Week%207%20-%20Analysing%20Web%20Data/W7D3%20-%20Mini%20project/"
    "Global%20Terrorism%20Database.zip"
)
GTD_ZIP = RAW_DIR / "global_terrorism_database.zip"

SELECTED_COLUMNS = [
    "eventid",
    "iyear",
    "imonth",
    "iday",
    "country_txt",
    "region_txt",
    "provstate",
    "city",
    "latitude",
    "longitude",
    "success",
    "suicide",
    "attacktype1_txt",
    "targtype1_txt",
    "weaptype1_txt",
    "gname",
    "individual",
    "nkill",
    "nwound",
    "property",
    "multiple",
    "extended",
]

WORLD_BANK_INDICATORS = {
    "NY.GDP.PCAP.CD": "gdp_per_capita_usd",
    "SP.POP.TOTL": "population",
    "SL.UEM.TOTL.ZS": "unemployment_pct",
}

COUNTRY_ALIASES = {
    "bahamas": "bahamas, the",
    "bolivia": "bolivia",
    "brunei": "brunei darussalam",
    "democratic republic of the congo": "congo, dem. rep.",
    "east germany": "germany",
    "egypt": "egypt, arab rep.",
    "gambia": "gambia, the",
    "hong kong": "hong kong sar, china",
    "iran": "iran, islamic rep.",
    "ivory coast": "cote d'ivoire",
    "kyrgyzstan": "kyrgyz republic",
    "laos": "lao pdr",
    "macau": "macao sar, china",
    "north korea": "korea, dem. people's rep.",
    "republic of the congo": "congo, rep.",
    "russia": "russian federation",
    "slovak republic": "slovak republic",
    "south korea": "korea, rep.",
    "syria": "syrian arab republic",
    "turkey": "turkiye",
    "venezuela": "venezuela, rb",
    "vietnam": "viet nam",
    "west bank and gaza strip": "west bank and gaza",
    "west germany": "germany",
    "yemen": "yemen, rep.",
}


@dataclass
class PipelineStats:
    raw_rows: int
    raw_columns: int
    duplicate_event_ids: int
    cleaned_rows: int
    integrated_rows: int
    world_bank_match_rate: float
    missing_casualties_before: int
    missing_casualties_after: int


def ensure_directories() -> None:
    for directory in [
        RAW_DIR,
        EXTRACTED_DIR,
        EXTERNAL_DIR,
        PROCESSED_DIR,
        SUMMARY_DIR,
        FIGURE_DIR,
    ]:
        directory.mkdir(parents=True, exist_ok=True)


def download_file(url: str, output_path: Path) -> None:
    if output_path.exists() and output_path.stat().st_size > 0:
        return

    print(f"Downloading {url}")
    with urllib.request.urlopen(url, timeout=120) as response:
        output_path.write_bytes(response.read())


def extract_zip(zip_path: Path, destination: Path) -> None:
    csv_files = list(destination.rglob("*.csv"))
    if csv_files:
        return

    print(f"Extracting {zip_path.name}")
    with zipfile.ZipFile(zip_path) as archive:
        archive.extractall(destination)


def find_gtd_csv() -> Path:
    csv_files = sorted(EXTRACTED_DIR.rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV file was found after extracting the GTD archive.")
    return csv_files[0]


def load_gtd(csv_path: Path) -> pd.DataFrame:
    print(f"Loading GTD from {csv_path}")
    return pd.read_csv(
        csv_path,
        encoding="ISO-8859-1",
        usecols=SELECTED_COLUMNS,
        low_memory=False,
    )


def normalize_country_name(value: object) -> str:
    if pd.isna(value):
        return ""

    normalized = str(value).strip().lower()
    normalized = normalized.replace("&", "and")
    normalized = re.sub(r"\s+", " ", normalized)
    normalized = normalized.removeprefix("the ")
    return COUNTRY_ALIASES.get(normalized, normalized)


def write_initial_assessment(raw: pd.DataFrame) -> None:
    dtype_rows = [
        {"column": column, "dtype": str(dtype)}
        for column, dtype in raw.dtypes.items()
    ]
    pd.DataFrame(dtype_rows).to_csv(SUMMARY_DIR / "initial_dtypes.csv", index=False)

    missing = (
        raw.isna()
        .sum()
        .reset_index()
        .rename(columns={"index": "column", 0: "missing_count"})
    )
    missing["missing_percent"] = (missing["missing_count"] / len(raw) * 100).round(2)
    missing.sort_values("missing_count", ascending=False).head(20).to_csv(
        SUMMARY_DIR / "missing_values_top20.csv",
        index=False,
    )


def clean_gtd(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df = df.drop_duplicates(subset=["eventid"]).copy()

    numeric_columns = [
        "iyear",
        "imonth",
        "iday",
        "latitude",
        "longitude",
        "success",
        "suicide",
        "individual",
        "nkill",
        "nwound",
        "property",
        "multiple",
        "extended",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["month_known"] = df["imonth"].between(1, 12)
    df["day_known"] = df["iday"].between(1, 31)
    df["event_month"] = df["imonth"].where(df["month_known"], 1).astype("Int64")
    df["event_day"] = df["iday"].where(df["day_known"], 1).astype("Int64")
    df["event_date"] = pd.to_datetime(
        {
            "year": df["iyear"],
            "month": df["event_month"],
            "day": df["event_day"],
        },
        errors="coerce",
    )

    df["latitude"] = df["latitude"].where(df["latitude"].between(-90, 90))
    df["longitude"] = df["longitude"].where(df["longitude"].between(-180, 180))
    df["has_coordinates"] = df["latitude"].notna() & df["longitude"].notna()

    categorical_columns = [
        "country_txt",
        "region_txt",
        "provstate",
        "city",
        "attacktype1_txt",
        "targtype1_txt",
        "weaptype1_txt",
        "gname",
    ]
    for column in categorical_columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA})
            .fillna("Unknown")
        )

    for column in ["success", "suicide", "individual", "property", "multiple", "extended"]:
        df[column] = df[column].fillna(0).astype(int)

    df["nkill_clean"] = df["nkill"].fillna(0).clip(lower=0)
    df["nwound_clean"] = df["nwound"].fillna(0).clip(lower=0)
    df["casualties"] = df["nkill_clean"] + df["nwound_clean"]
    df["fatal_attack"] = (df["nkill_clean"] > 0).astype(int)
    df["mass_casualty_attack"] = (df["casualties"] >= 10).astype(int)
    df["country_norm"] = df["country_txt"].map(normalize_country_name)

    return df


def add_transformations(cleaned: pd.DataFrame) -> pd.DataFrame:
    df = cleaned.copy()

    df["casualties_log1p"] = df["casualties"].map(lambda value: math.log1p(float(value)))
    for column in ["nkill_clean", "nwound_clean", "casualties", "casualties_log1p"]:
        mean = df[column].mean()
        std = df[column].std()
        df[f"{column}_zscore"] = 0 if std == 0 else (df[column] - mean) / std

    dummy_source = df[["attacktype1_txt", "targtype1_txt", "weaptype1_txt"]]
    dummies = pd.get_dummies(
        dummy_source,
        prefix=["attack", "target", "weapon"],
        dtype=int,
    )
    return pd.concat([df, dummies], axis=1)


def fetch_world_bank_indicator(indicator: str, value_name: str) -> pd.DataFrame:
    cache_path = EXTERNAL_DIR / f"world_bank_{indicator}.csv"
    if cache_path.exists() and cache_path.stat().st_size > 0:
        return pd.read_csv(cache_path)

    url = (
        f"https://api.worldbank.org/v2/country/all/indicator/{indicator}"
        "?format=json&per_page=20000"
    )
    print(f"Downloading World Bank indicator {indicator}")
    with urllib.request.urlopen(url, timeout=120) as response:
        payload = json.loads(response.read().decode("utf-8"))

    rows = []
    for record in payload[1]:
        country = record.get("country") or {}
        rows.append(
            {
                "country": country.get("value"),
                "country_norm": normalize_country_name(country.get("value")),
                "country_iso3": record.get("countryiso3code"),
                "iyear": int(record["date"]),
                value_name: record.get("value"),
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv(cache_path, index=False)
    return df


def load_world_bank_context() -> pd.DataFrame:
    merged: pd.DataFrame | None = None

    for indicator, value_name in WORLD_BANK_INDICATORS.items():
        indicator_df = fetch_world_bank_indicator(indicator, value_name)
        indicator_df = indicator_df[["country_norm", "country_iso3", "iyear", value_name]]

        if merged is None:
            merged = indicator_df
        else:
            merged = merged.merge(
                indicator_df,
                on=["country_norm", "country_iso3", "iyear"],
                how="outer",
            )

    if merged is None:
        raise RuntimeError("World Bank context could not be loaded.")

    return merged.drop_duplicates(subset=["country_norm", "iyear"])


def integrate_context(transformed: pd.DataFrame, context: pd.DataFrame) -> pd.DataFrame:
    integrated = transformed.merge(
        context,
        on=["country_norm", "iyear"],
        how="left",
        suffixes=("", "_world_bank"),
    )

    for column in ["gdp_per_capita_usd", "population", "unemployment_pct"]:
        integrated[column] = pd.to_numeric(integrated[column], errors="coerce")

    integrated["gdp_per_capita_log1p"] = integrated["gdp_per_capita_usd"].map(
        lambda value: math.log1p(value) if pd.notna(value) and value >= 0 else pd.NA
    )
    return integrated


def save_processed_datasets(integrated: pd.DataFrame) -> None:
    full_output = PROCESSED_DIR / "gtd_clean_integrated.csv"
    sample_output = PROCESSED_DIR / "gtd_model_ready_sample.csv"

    integrated.to_csv(full_output, index=False)

    model_columns = [
        "eventid",
        "iyear",
        "event_date",
        "country_txt",
        "region_txt",
        "attacktype1_txt",
        "targtype1_txt",
        "weaptype1_txt",
        "success",
        "suicide",
        "fatal_attack",
        "mass_casualty_attack",
        "nkill_clean",
        "nwound_clean",
        "casualties",
        "casualties_zscore",
        "gdp_per_capita_usd",
        "population",
        "unemployment_pct",
    ]
    dummy_columns = [
        column
        for column in integrated.columns
        if column.startswith(("attack_", "target_", "weapon_"))
    ]
    sample_columns = model_columns + dummy_columns
    integrated[sample_columns].head(5000).to_csv(sample_output, index=False)


def summarize(integrated: pd.DataFrame) -> dict[str, pd.DataFrame]:
    yearly = (
        integrated.groupby("iyear", as_index=False)
        .agg(
            attacks=("eventid", "count"),
            fatalities=("nkill_clean", "sum"),
            wounded=("nwound_clean", "sum"),
            casualties=("casualties", "sum"),
        )
        .sort_values("iyear")
    )

    region = (
        integrated.groupby("region_txt", as_index=False)
        .agg(
            attacks=("eventid", "count"),
            fatalities=("nkill_clean", "sum"),
            casualties=("casualties", "sum"),
            success_rate=("success", "mean"),
            suicide_rate=("suicide", "mean"),
        )
        .sort_values("attacks", ascending=False)
    )
    region["success_rate"] = (region["success_rate"] * 100).round(2)
    region["suicide_rate"] = (region["suicide_rate"] * 100).round(2)

    country = (
        integrated.groupby("country_txt", as_index=False)
        .agg(
            attacks=("eventid", "count"),
            fatalities=("nkill_clean", "sum"),
            casualties=("casualties", "sum"),
            avg_gdp_per_capita_usd=("gdp_per_capita_usd", "mean"),
            avg_unemployment_pct=("unemployment_pct", "mean"),
        )
        .sort_values("attacks", ascending=False)
        .head(20)
    )

    attack_type = (
        integrated.groupby("attacktype1_txt", as_index=False)
        .agg(
            attacks=("eventid", "count"),
            fatalities=("nkill_clean", "sum"),
            avg_casualties=("casualties", "mean"),
        )
        .sort_values("attacks", ascending=False)
    )
    attack_type["avg_casualties"] = attack_type["avg_casualties"].round(2)

    socio = integrated.dropna(subset=["gdp_per_capita_usd"]).copy()
    socio["gdp_band"] = pd.qcut(
        socio["gdp_per_capita_usd"],
        q=4,
        labels=["Lowest GDP pc", "Low-mid GDP pc", "High-mid GDP pc", "Highest GDP pc"],
        duplicates="drop",
    )
    socioeconomic = (
        socio.groupby("gdp_band", observed=True, as_index=False)
        .agg(
            attacks=("eventid", "count"),
            fatalities=("nkill_clean", "sum"),
            avg_casualties=("casualties", "mean"),
            avg_unemployment_pct=("unemployment_pct", "mean"),
        )
        .sort_values("attacks", ascending=False)
    )
    socioeconomic["avg_casualties"] = socioeconomic["avg_casualties"].round(2)
    socioeconomic["avg_unemployment_pct"] = socioeconomic["avg_unemployment_pct"].round(2)

    summaries = {
        "yearly_attacks": yearly,
        "region_summary": region,
        "country_summary_top20": country,
        "attack_type_summary": attack_type,
        "socioeconomic_summary": socioeconomic,
    }
    for name, frame in summaries.items():
        frame.to_csv(SUMMARY_DIR / f"{name}.csv", index=False)

    return summaries


def svg_escape(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def save_bar_chart(
    data: pd.DataFrame,
    label_column: str,
    value_column: str,
    title: str,
    output_path: Path,
    limit: int = 12,
) -> None:
    chart = data[[label_column, value_column]].head(limit).copy()
    chart[value_column] = pd.to_numeric(chart[value_column], errors="coerce").fillna(0)

    width = 980
    row_height = 34
    left = 230
    right = 40
    top = 62
    height = top + len(chart) * row_height + 42
    max_value = max(float(chart[value_column].max()), 1)
    bar_width = width - left - right

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="24" y="34" font-family="Arial" font-size="22" font-weight="700" fill="#1f2937">{svg_escape(title)}</text>',
    ]

    for index, row in enumerate(chart.itertuples(index=False)):
        label = getattr(row, label_column)
        value = float(getattr(row, value_column))
        y = top + index * row_height
        current_width = 0 if max_value == 0 else value / max_value * bar_width
        parts.extend(
            [
                f'<text x="24" y="{y + 20}" font-family="Arial" font-size="13" fill="#374151">{svg_escape(label)}</text>',
                f'<rect x="{left}" y="{y}" width="{current_width:.1f}" height="22" rx="3" fill="#2563eb"/>',
                f'<text x="{left + current_width + 8}" y="{y + 16}" font-family="Arial" font-size="12" fill="#111827">{value:,.0f}</text>',
            ]
        )

    parts.append("</svg>")
    output_path.write_text("\n".join(parts), encoding="utf-8")


def save_line_chart(
    data: pd.DataFrame,
    x_column: str,
    y_column: str,
    title: str,
    output_path: Path,
) -> None:
    chart = data[[x_column, y_column]].dropna().sort_values(x_column)
    width = 980
    height = 430
    left = 60
    right = 30
    top = 62
    bottom = 58
    plot_width = width - left - right
    plot_height = height - top - bottom
    x_min = float(chart[x_column].min())
    x_max = float(chart[x_column].max())
    y_max = max(float(chart[y_column].max()), 1)

    points = []
    for row in chart.itertuples(index=False):
        x_value = float(getattr(row, x_column))
        y_value = float(getattr(row, y_column))
        x = left + (x_value - x_min) / (x_max - x_min) * plot_width
        y = top + plot_height - (y_value / y_max * plot_height)
        points.append(f"{x:.1f},{y:.1f}")

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        f'<text x="24" y="34" font-family="Arial" font-size="22" font-weight="700" fill="#1f2937">{svg_escape(title)}</text>',
        f'<line x1="{left}" y1="{top + plot_height}" x2="{width - right}" y2="{top + plot_height}" stroke="#9ca3af"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" stroke="#9ca3af"/>',
        f'<polyline points="{" ".join(points)}" fill="none" stroke="#dc2626" stroke-width="3"/>',
        f'<text x="{left}" y="{height - 20}" font-family="Arial" font-size="12" fill="#374151">{int(x_min)}</text>',
        f'<text x="{width - right - 30}" y="{height - 20}" font-family="Arial" font-size="12" fill="#374151">{int(x_max)}</text>',
        f'<text x="12" y="{top + 12}" font-family="Arial" font-size="12" fill="#374151">{y_max:,.0f}</text>',
        f'<text x="12" y="{top + plot_height}" font-family="Arial" font-size="12" fill="#374151">0</text>',
        "</svg>",
    ]
    output_path.write_text("\n".join(parts), encoding="utf-8")


def save_visualizations(summaries: dict[str, pd.DataFrame]) -> None:
    save_line_chart(
        summaries["yearly_attacks"],
        "iyear",
        "attacks",
        "Terrorism Events by Year",
        FIGURE_DIR / "yearly_attacks.svg",
    )
    save_bar_chart(
        summaries["region_summary"],
        "region_txt",
        "attacks",
        "Events by Region",
        FIGURE_DIR / "attacks_by_region.svg",
    )
    save_bar_chart(
        summaries["country_summary_top20"],
        "country_txt",
        "attacks",
        "Top 20 Countries by Event Count",
        FIGURE_DIR / "top_countries.svg",
        limit=20,
    )
    save_bar_chart(
        summaries["attack_type_summary"],
        "attacktype1_txt",
        "attacks",
        "Events by Attack Type",
        FIGURE_DIR / "attack_types.svg",
    )
    save_bar_chart(
        summaries["socioeconomic_summary"],
        "gdp_band",
        "attacks",
        "Events by GDP per Capita Band",
        FIGURE_DIR / "events_by_gdp_band.svg",
        limit=4,
    )


def write_markdown_table(rows: Iterable[dict[str, object]], columns: list[str]) -> str:
    def markdown_escape(value: object) -> str:
        if pd.isna(value):
            return ""

        text = str(value)
        text = text.replace("|", "\\|")
        if text.endswith(".0") and text[:-2].replace("-", "").isdigit():
            text = text[:-2]
        return text

    output = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows:
        output.append(
            "| "
            + " | ".join(markdown_escape(row.get(column, "")) for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_report(stats: PipelineStats, summaries: dict[str, pd.DataFrame]) -> None:
    top_regions = summaries["region_summary"].head(5).to_dict("records")
    top_attacks = summaries["attack_type_summary"].head(5).to_dict("records")
    top_countries = summaries["country_summary_top20"].head(10).to_dict("records")
    peak_year = summaries["yearly_attacks"].sort_values("attacks", ascending=False).iloc[0]

    report = f"""# Global Terrorism Database: Cleaning, Transformation, and Integration Report

## Overview

This project prepares the Global Terrorism Database for analysis and integrates it with World Bank country-year socio-economic indicators. The final integrated dataset is saved locally under `data/processed/`, while the large `data/` folder is excluded from git.

## Initial Assessment

- Raw rows loaded: {stats.raw_rows:,}
- Raw columns loaded for this analysis: {stats.raw_columns:,}
- Duplicate event IDs found: {stats.duplicate_event_ids:,}
- Missing `nkill`/`nwound` values before cleaning: {stats.missing_casualties_before:,}
- Rows after cleaning: {stats.cleaned_rows:,}

The initial assessment files are:

- `outputs/summaries/initial_dtypes.csv`
- `outputs/summaries/missing_values_top20.csv`

## Cleaning Decisions

- Removed duplicate records using `eventid`.
- Converted year, month, day, coordinates, indicators, and casualty columns to numeric types.
- Treated month/day values of `0` as unknown and used `1` only to build a usable approximate `event_date`.
- Preserved `month_known` and `day_known` flags so date uncertainty is not hidden.
- Replaced missing categorical values with `Unknown`.
- Filled missing fatalities and injuries with `0` for analysis-ready casualty totals.
- Removed invalid latitude and longitude values by setting out-of-range coordinates to missing.
- Added `has_coordinates`, `fatal_attack`, and `mass_casualty_attack` indicators.

## Transformation Decisions

- One-hot encoded attack type, target type, and weapon type categories.
- Created `casualties` and `casualties_log1p`.
- Standardized `nkill_clean`, `nwound_clean`, `casualties`, and `casualties_log1p` with z-scores.

## Integrated Dataset

The cleaned GTD data was integrated with World Bank indicators by normalized country name and year.

- Integrated rows: {stats.integrated_rows:,}
- Rows matched to at least one World Bank GDP-per-capita value: {stats.world_bank_match_rate:.2f}%
- Added context fields: `gdp_per_capita_usd`, `population`, `unemployment_pct`, and `gdp_per_capita_log1p`.

## Exploratory Highlights

- Peak event year: {int(peak_year["iyear"])} with {int(peak_year["attacks"]):,} events.

### Top Regions

{write_markdown_table(top_regions, ["region_txt", "attacks", "fatalities", "casualties", "success_rate", "suicide_rate"])}

### Top Countries

{write_markdown_table(top_countries, ["country_txt", "attacks", "fatalities", "casualties"])}

### Top Attack Types

{write_markdown_table(top_attacks, ["attacktype1_txt", "attacks", "fatalities", "avg_casualties"])}

## Visualizations

- `outputs/figures/yearly_attacks.svg`
- `outputs/figures/attacks_by_region.svg`
- `outputs/figures/top_countries.svg`
- `outputs/figures/attack_types.svg`
- `outputs/figures/events_by_gdp_band.svg`

## Limitations

- GTD has known uncertainty in exact dates, perpetrators, and casualty totals, so uncertainty flags should be considered during analysis.
- Country-name integration with World Bank data is normalized but not perfect; some historical or disputed territories may not match.
- Filling missing casualty values with zero is useful for aggregate analysis, but a stricter research project may keep missing and zero casualties separate.
"""

    (PROJECT_ROOT / "report.md").write_text(report, encoding="utf-8")


def main() -> None:
    ensure_directories()
    download_file(GTD_URL, GTD_ZIP)
    extract_zip(GTD_ZIP, EXTRACTED_DIR)

    gtd_csv = find_gtd_csv()
    raw = load_gtd(gtd_csv)
    write_initial_assessment(raw)

    duplicate_event_ids = int(raw["eventid"].duplicated().sum())
    missing_casualties_before = int(raw[["nkill", "nwound"]].isna().sum().sum())

    cleaned = clean_gtd(raw)
    transformed = add_transformations(cleaned)
    world_bank_context = load_world_bank_context()
    integrated = integrate_context(transformed, world_bank_context)

    missing_casualties_after = int(
        integrated[["nkill_clean", "nwound_clean"]].isna().sum().sum()
    )
    world_bank_match_rate = (
        integrated["gdp_per_capita_usd"].notna().mean() * 100
    )

    save_processed_datasets(integrated)
    summaries = summarize(integrated)
    save_visualizations(summaries)

    stats = PipelineStats(
        raw_rows=len(raw),
        raw_columns=len(raw.columns),
        duplicate_event_ids=duplicate_event_ids,
        cleaned_rows=len(cleaned),
        integrated_rows=len(integrated),
        world_bank_match_rate=world_bank_match_rate,
        missing_casualties_before=missing_casualties_before,
        missing_casualties_after=missing_casualties_after,
    )
    write_report(stats, summaries)

    print("Done.")
    print(f"Clean integrated dataset: {PROCESSED_DIR / 'gtd_clean_integrated.csv'}")
    print(f"Report: {PROJECT_ROOT / 'report.md'}")


if __name__ == "__main__":
    main()
