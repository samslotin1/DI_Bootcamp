from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "global_power_plant_database.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
REPORT_PATH = BASE_DIR / "global_power_plant_report.md"

NUMERIC_COLUMNS = [
    "capacity_mw",
    "latitude",
    "longitude",
    "commissioning_year",
    "year_of_capacity_data",
    "generation_gwh_2013",
    "generation_gwh_2014",
    "generation_gwh_2015",
    "generation_gwh_2016",
    "generation_gwh_2017",
    "generation_gwh_2018",
    "generation_gwh_2019",
    "estimated_generation_gwh_2013",
    "estimated_generation_gwh_2014",
    "estimated_generation_gwh_2015",
    "estimated_generation_gwh_2016",
    "estimated_generation_gwh_2017",
]


def markdown_table(dataframe, max_rows=12, float_format="{:,.2f}"):
    table = dataframe.head(max_rows).copy()

    def format_value(value):
        if pd.isna(value):
            return ""
        if isinstance(value, (float, np.floating)):
            return float_format.format(value)
        if isinstance(value, (int, np.integer)):
            return f"{value:,}"
        return str(value)

    headers = [str(column) for column in table.columns]
    rows = [
        [format_value(value) for value in row]
        for row in table.itertuples(index=False, name=None)
    ]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def save_plot(path):
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()


def load_and_clean_data():
    df = pd.read_csv(DATA_PATH, low_memory=False)
    original_shape = df.shape

    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    text_columns = df.select_dtypes(include=["object", "string"]).columns
    for column in text_columns:
        df[column] = df[column].fillna("Unknown")

    df["capacity_mw"] = df["capacity_mw"].replace([np.inf, -np.inf], np.nan)
    df = df[df["capacity_mw"].notna() & (df["capacity_mw"] > 0)].copy()
    df["commissioning_year"] = df["commissioning_year"].where(
        df["commissioning_year"].between(1800, 2025)
    )

    return df, original_shape


def create_visualizations(df):
    sns.set_theme(style="whitegrid")
    OUTPUT_DIR.mkdir(exist_ok=True)

    top_countries = df["country_long"].value_counts().head(15)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_countries.values, y=top_countries.index, hue=top_countries.index, legend=False)
    plt.title("Top 15 Countries by Number of Power Plants")
    plt.xlabel("Number of plants")
    plt.ylabel("Country")
    save_plot(OUTPUT_DIR / "top_countries_by_plant_count.png")

    top_fuels = df["primary_fuel"].value_counts().head(10).index
    fuel_subset = df[df["primary_fuel"].isin(top_fuels)].copy()
    fuel_subset["log_capacity_mw"] = np.log10(fuel_subset["capacity_mw"])
    plt.figure(figsize=(11, 6))
    sns.boxplot(data=fuel_subset, x="primary_fuel", y="log_capacity_mw")
    plt.title("Capacity Distribution by Top Fuel Types")
    plt.xlabel("Primary fuel")
    plt.ylabel("log10(capacity MW)")
    plt.xticks(rotation=35, ha="right")
    save_plot(OUTPUT_DIR / "capacity_distribution_by_fuel.png")

    time_df = df.dropna(subset=["commissioning_year"]).copy()
    time_df["decade"] = (time_df["commissioning_year"] // 10 * 10).astype(int)
    recent_decades = time_df[time_df["decade"].between(1950, 2020)]
    fuel_mix = (
        recent_decades.pivot_table(
            index="decade",
            columns="primary_fuel",
            values="capacity_mw",
            aggfunc="sum",
            fill_value=0,
        )
        .loc[:, lambda data: data.sum().sort_values(ascending=False).head(8).index]
    )
    fuel_mix_share = fuel_mix.div(fuel_mix.sum(axis=1), axis=0)
    fuel_mix_share.plot(kind="bar", stacked=True, figsize=(12, 6), colormap="tab20")
    plt.title("Fuel Mix by Commissioning Decade, Capacity Share")
    plt.xlabel("Commissioning decade")
    plt.ylabel("Share of commissioned capacity")
    plt.legend(title="Fuel", bbox_to_anchor=(1.02, 1), loc="upper left")
    save_plot(OUTPUT_DIR / "fuel_mix_by_decade.png")

    map_fuels = df["primary_fuel"].value_counts().head(7).index
    map_df = df[df["primary_fuel"].isin(map_fuels)].sample(
        n=min(12000, len(df)),
        random_state=42,
    )
    plt.figure(figsize=(12, 6))
    sns.scatterplot(
        data=map_df,
        x="longitude",
        y="latitude",
        hue="primary_fuel",
        size="capacity_mw",
        sizes=(8, 140),
        alpha=0.55,
        linewidth=0,
    )
    plt.title("Geographical Distribution of Power Plants")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    save_plot(OUTPUT_DIR / "geographical_distribution.png")

    corr_columns = ["capacity_mw", "latitude", "longitude", "commissioning_year"]
    corr_df = df[corr_columns].dropna().copy()
    corr_df["log_capacity_mw"] = np.log1p(corr_df["capacity_mw"])
    corr = corr_df[["log_capacity_mw", "latitude", "longitude", "commissioning_year"]].corr()
    plt.figure(figsize=(7, 5))
    sns.heatmap(corr, annot=True, cmap="vlag", center=0, fmt=".2f")
    plt.title("Correlation Matrix for Key Numeric Attributes")
    save_plot(OUTPUT_DIR / "numeric_correlation_heatmap.png")


def run_analysis():
    df, original_shape = load_and_clean_data()

    missing_before = pd.read_csv(DATA_PATH, low_memory=False).isna().sum().sort_values(ascending=False)
    missing_after = df.isna().sum().sort_values(ascending=False)

    numeric_summary = df[NUMERIC_COLUMNS].agg(["mean", "median", "std"]).T
    country_distribution = (
        df["country_long"].value_counts().head(15).rename_axis("country").reset_index(name="plant_count")
    )
    fuel_distribution = (
        df["primary_fuel"].value_counts().rename_axis("primary_fuel").reset_index(name="plant_count")
    )

    fuel_capacity = (
        df.groupby("primary_fuel")["capacity_mw"]
        .agg(["count", "mean", "median", "std", "sum"])
        .sort_values("sum", ascending=False)
    )

    top_fuels_for_test = fuel_capacity[fuel_capacity["count"] >= 30].head(6).index.tolist()
    capacity_groups = [
        df.loc[df["primary_fuel"] == fuel, "capacity_mw"].to_numpy()
        for fuel in top_fuels_for_test
    ]
    anova_result = stats.f_oneway(*capacity_groups)
    kruskal_result = stats.kruskal(*capacity_groups)
    coal_gas_ttest = stats.ttest_ind(
        df.loc[df["primary_fuel"] == "Coal", "capacity_mw"].to_numpy(),
        df.loc[df["primary_fuel"] == "Gas", "capacity_mw"].to_numpy(),
        equal_var=False,
    )

    time_df = df.dropna(subset=["commissioning_year"]).copy()
    time_df["commissioning_year"] = time_df["commissioning_year"].astype(int)
    yearly_capacity = (
        time_df.groupby("commissioning_year")["capacity_mw"]
        .agg(["count", "sum", "mean"])
        .loc[lambda data: data.index >= 1950]
    )
    time_df["decade"] = (time_df["commissioning_year"] // 10 * 10).astype(int)
    decade_fuel_mix = (
        time_df[time_df["decade"].between(1950, 2020)]
        .pivot_table(
            index="decade",
            columns="primary_fuel",
            values="capacity_mw",
            aggfunc="sum",
            fill_value=0,
        )
    )
    decade_fuel_mix = decade_fuel_mix.loc[
        :, decade_fuel_mix.sum().sort_values(ascending=False).head(10).index
    ]
    decade_fuel_share = decade_fuel_mix.div(decade_fuel_mix.sum(axis=1), axis=0)

    # NumPy filtering example: plants above the 95th capacity percentile.
    capacity_array = df["capacity_mw"].to_numpy()
    high_capacity_cutoff = np.percentile(capacity_array, 95)
    high_capacity_mask = capacity_array >= high_capacity_cutoff
    high_capacity_plants = df.loc[high_capacity_mask, ["country_long", "name", "primary_fuel", "capacity_mw"]]

    # Matrix operation: country x fuel capacity matrix and fuel similarity matrix.
    country_fuel_matrix = df.pivot_table(
        index="country_long",
        columns="primary_fuel",
        values="capacity_mw",
        aggfunc="sum",
        fill_value=0,
    )
    matrix = country_fuel_matrix.to_numpy(dtype=float)
    norms = np.linalg.norm(matrix, axis=0)
    safe_norms = np.where(norms == 0, 1, norms)
    fuel_similarity = (matrix.T @ matrix) / np.outer(safe_norms, safe_norms)
    fuel_similarity_df = pd.DataFrame(
        fuel_similarity,
        index=country_fuel_matrix.columns,
        columns=country_fuel_matrix.columns,
    )

    pca_data = df[["capacity_mw", "latitude", "longitude", "commissioning_year"]].dropna().copy()
    pca_data["log_capacity_mw"] = np.log1p(pca_data["capacity_mw"])
    feature_matrix = pca_data[["log_capacity_mw", "latitude", "longitude", "commissioning_year"]].to_numpy()
    standardized = (feature_matrix - feature_matrix.mean(axis=0)) / feature_matrix.std(axis=0)
    covariance_matrix = np.cov(standardized, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:, order]
    explained_variance = eigenvalues / eigenvalues.sum()
    eigen_summary = pd.DataFrame(
        {
            "component": [f"PC{i + 1}" for i in range(len(eigenvalues))],
            "eigenvalue": eigenvalues,
            "explained_variance_share": explained_variance,
        }
    )

    create_visualizations(df)

    report = f"""# Global Power Plant Database Analysis

## 1. Data Import and Cleaning

The dataset was imported with Pandas from `global_power_plant_database.csv`.

- Original shape: `{original_shape[0]:,}` rows and `{original_shape[1]:,}` columns
- Cleaned shape used for analysis: `{df.shape[0]:,}` rows and `{df.shape[1]:,}` columns
- Numeric columns were converted with `pd.to_numeric(..., errors="coerce")`
- Text missing values were filled with `Unknown`
- Invalid or missing `capacity_mw` rows were removed because capacity is the main output metric
- Implausible `commissioning_year` values outside 1800-2025 were treated as missing

### Missing Values Before Cleaning

{markdown_table(missing_before.reset_index().rename(columns={"index": "column", 0: "missing_values"}), 12)}

### Missing Values After Cleaning

{markdown_table(missing_after.reset_index().rename(columns={"index": "column", 0: "missing_values"}), 12)}

## 2. Exploratory Data Analysis

### Numerical Summary

{markdown_table(numeric_summary.reset_index().rename(columns={"index": "column"}), 12)}

### Top Countries by Number of Plants

{markdown_table(country_distribution, 15)}

### Power Plants by Fuel Type

{markdown_table(fuel_distribution, 15)}

The dataset is dominated by Hydro, Solar, Wind, Gas, Coal, and Oil plants by count. By total capacity, large thermal and hydro plants carry much more weight than their plant counts alone suggest.

## 3. Statistical Analysis

### Capacity by Fuel Type

{markdown_table(fuel_capacity.reset_index().rename(columns={"index": "primary_fuel"}), 15)}

Hypothesis test:

- Null hypothesis: mean `capacity_mw` is equal across the tested fuel types.
- Alternative hypothesis: at least one tested fuel type has a different mean capacity.
- Fuel types tested: `{", ".join(top_fuels_for_test)}`
- One-way ANOVA statistic: `{anova_result.statistic:,.3f}`
- One-way ANOVA p-value: `{anova_result.pvalue:.3e}`
- Kruskal-Wallis statistic: `{kruskal_result.statistic:,.3f}`
- Kruskal-Wallis p-value: `{kruskal_result.pvalue:.3e}`
- Welch t-test, Coal vs Gas p-value: `{coal_gas_ttest.pvalue:.3e}`

Because the p-values are far below 0.05, we reject the null hypothesis. The average power output capacity differs significantly between major fuel types.

## 4. Time Series Analysis

The dataset includes `commissioning_year`, which can be used as an approximate establishment year. Missing years were excluded from this part only.

### Recent Yearly Capacity Summary

{markdown_table(yearly_capacity.tail(12).reset_index(), 12)}

### Fuel Mix by Commissioning Decade

{markdown_table(decade_fuel_share.tail(8).reset_index(), 8, float_format="{:.2%}")}

The time trend shows that older commissioned capacity is heavily represented by Hydro, Coal, Gas, and Nuclear. In recent decades, Solar and Wind take a much larger share of newly commissioned plants and capacity.

## 5. Advanced Visualization

Charts were saved in the `outputs` folder:

- `top_countries_by_plant_count.png`
- `capacity_distribution_by_fuel.png`
- `fuel_mix_by_decade.png`
- `geographical_distribution.png`
- `numeric_correlation_heatmap.png`

![Top countries by plant count](outputs/top_countries_by_plant_count.png)

![Capacity distribution by fuel](outputs/capacity_distribution_by_fuel.png)

![Fuel mix by decade](outputs/fuel_mix_by_decade.png)

![Geographical distribution](outputs/geographical_distribution.png)

![Numeric correlation heatmap](outputs/numeric_correlation_heatmap.png)

The geographic plot uses longitude and latitude to show global plant locations. Capacity is represented by marker size and major fuel types are represented by color.

## 6. Matrix Operations in a Real-World Context

Two matrix examples were created with NumPy:

1. A country-by-fuel capacity matrix where each row is a country and each column is a primary fuel type. Multiplying `matrix.T @ matrix` produces a fuel relationship matrix showing which fuel types tend to appear in the same national capacity profiles.
2. A standardized numeric feature matrix using log capacity, latitude, longitude, and commissioning year. The covariance matrix was decomposed into eigenvalues and eigenvectors.

### Eigenvalue Summary

{markdown_table(eigen_summary, 4)}

Eigenvectors are useful here because they define the principal directions of variation in the numeric data. Eigenvalues show how much variance each direction explains. In a real-world energy analysis, this is relevant for dimensionality reduction, clustering countries or plants, and identifying whether geography, plant age, or capacity size explains most of the numeric variation. These components are descriptive, not causal.

## 7. Integrating NumPy with Pandas and Matplotlib

Examples used in the analysis:

- `np.percentile` was used to find the 95th percentile capacity cutoff: `{high_capacity_cutoff:,.2f}` MW.
- A NumPy boolean mask selected `{high_capacity_mask.sum():,}` high-capacity plants from the Pandas DataFrame.
- `np.log10` and `np.log1p` were used to make skewed capacity values easier to visualize and analyze.
- `np.linalg.norm`, matrix multiplication, covariance matrices, eigenvalues, and eigenvectors were used for relationship analysis.

### Sample of High-Capacity Plants

{markdown_table(high_capacity_plants.sort_values("capacity_mw", ascending=False), 10)}

## Conclusion

The global power plant dataset contains broad coverage across countries and fuel types, but it has meaningful missingness in commissioning year, owner, WEPP identifiers, and reported generation. After cleaning the core analytical fields, fuel type is strongly associated with plant capacity. The statistical tests show significant differences in mean capacity between major fuel types. Over time, the energy mix shifts toward more Solar and Wind in newer commissioning decades, while older capacity is more concentrated in Hydro, Coal, Gas, and Nuclear. Matrix operations and eigenvalue analysis provide a compact way to study relationships among capacity, geography, and age of plants.
"""

    REPORT_PATH.write_text(report, encoding="utf-8")

    fuel_capacity.to_csv(OUTPUT_DIR / "capacity_by_fuel_type.csv")
    country_distribution.to_csv(OUTPUT_DIR / "top_countries_by_plant_count.csv", index=False)
    decade_fuel_share.to_csv(OUTPUT_DIR / "fuel_mix_by_decade_share.csv")
    fuel_similarity_df.to_csv(OUTPUT_DIR / "fuel_similarity_matrix.csv")
    eigen_summary.to_csv(OUTPUT_DIR / "eigenvalue_summary.csv", index=False)

    print(f"Report written to: {REPORT_PATH}")
    print(f"Outputs written to: {OUTPUT_DIR}")


if __name__ == "__main__":
    run_analysis()
