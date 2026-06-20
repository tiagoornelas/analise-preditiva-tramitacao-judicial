from __future__ import annotations

import pandas as pd

from . import config
from .utils import ensure_project_directories, save_csv, save_markdown


def load_modeling_dataset() -> pd.DataFrame:
    return pd.read_csv(config.PROCESSED_DATA_DIR / "modeling_dataset.csv")


def descriptive_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    columns = [config.TARGET_COLUMN, "procel1", "iad1", "cm1", "sajudmag1", "cn1", "g1", "h1"]
    return dataframe[columns].describe().transpose().reset_index(names="variable")


def branch_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    return (
        dataframe.groupby(config.BRANCH_COLUMN)
        .agg(
            rows=(config.TARGET_COLUMN, "size"),
            mean_target=(config.TARGET_COLUMN, "mean"),
            median_target=(config.TARGET_COLUMN, "median"),
            mean_digitalization=("procel1", "mean"),
            mean_iad=("iad1", "mean"),
        )
        .reset_index()
        .sort_values(config.BRANCH_COLUMN)
    )


def yearly_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    return (
        dataframe.groupby(config.YEAR_COLUMN)
        .agg(
            rows=(config.TARGET_COLUMN, "size"),
            mean_target=(config.TARGET_COLUMN, "mean"),
            mean_digitalization=("procel1", "mean"),
            mean_new_cases=("cn1", "mean"),
        )
        .reset_index()
        .sort_values(config.YEAR_COLUMN)
    )


def correlation_summary(dataframe: pd.DataFrame) -> pd.DataFrame:
    columns = [config.TARGET_COLUMN, "procel1", "iad1", "cm1", "sajudmag1", "cn1", "g1", "h1", config.YEAR_COLUMN]
    correlation = dataframe[columns].corr(numeric_only=True)
    return correlation.reset_index(names="variable")


def write_exploration_note(branches: pd.DataFrame, years: pd.DataFrame) -> None:
    note = f"""# Exploratory analysis note

## Branch summary

{branches.to_markdown(index=False)}

## Yearly summary

{years.to_markdown(index=False)}

## Interpretation prompts

1. Compare whether average digitalization rises over time while mean target decreases.
2. Compare whether Federal and Trabalho branches differ from Estadual in the mean target.
3. Check whether higher IAD tracks lower target values.
"""
    save_markdown(note, config.TECHNICAL_NOTES_DIR / "exploratory-analysis.md")


def main() -> None:
    ensure_project_directories()
    dataframe = load_modeling_dataset()

    descriptive = descriptive_summary(dataframe)
    branches = branch_summary(dataframe)
    years = yearly_summary(dataframe)
    correlation = correlation_summary(dataframe)

    save_csv(descriptive, config.TABLES_DIR / "descriptive_summary.csv")
    save_csv(branches, config.TABLES_DIR / "branch_summary.csv")
    save_csv(years, config.TABLES_DIR / "yearly_summary.csv")
    save_csv(correlation, config.TABLES_DIR / "correlation_matrix.csv")

    write_exploration_note(branches, years)
    print("Saved exploratory summaries.")


if __name__ == "__main__":
    main()
