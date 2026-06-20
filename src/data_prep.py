from __future__ import annotations

import json

import pandas as pd

from . import config
from .utils import (
    coerce_numeric_columns,
    dataset_scope_mask,
    ensure_project_directories,
    load_main_dataset,
    load_variable_dictionary,
    replace_nd_with_missing,
    save_csv,
    save_markdown,
)


def build_modeling_dataset() -> pd.DataFrame:
    raw = load_main_dataset()
    raw = replace_nd_with_missing(raw)
    filtered = raw.loc[dataset_scope_mask(raw)].copy()

    selected_columns = list(dict.fromkeys(config.MODEL_COLUMNS + config.NUMERIC_FEATURES + config.CATEGORICAL_FEATURES))
    dataset = filtered[selected_columns].copy()
    dataset = coerce_numeric_columns(dataset, [config.TARGET_COLUMN, *config.NUMERIC_FEATURES])
    dataset["dsc_tribunal"] = dataset["dsc_tribunal"].fillna(dataset[config.TRIBUNAL_COLUMN])
    dataset = dataset.dropna(subset=[config.TARGET_COLUMN])

    return dataset.sort_values([config.YEAR_COLUMN, config.BRANCH_COLUMN, config.TRIBUNAL_COLUMN]).reset_index(drop=True)


def build_missingness_table(dataframe: pd.DataFrame) -> pd.DataFrame:
    missing_count = dataframe.isna().sum()
    missing_ratio = dataframe.isna().mean().round(4)

    return pd.DataFrame(
        {
            "column": missing_count.index,
            "missing_count": missing_count.values,
            "missing_ratio": missing_ratio.values,
        }
    ).sort_values(["missing_ratio", "column"], ascending=[False, True])


def build_scope_summary(dataframe: pd.DataFrame) -> dict[str, object]:
    return {
        "rows": int(len(dataframe)),
        "branches": sorted(dataframe[config.BRANCH_COLUMN].dropna().unique().tolist()),
        "tribunals": int(dataframe[config.TRIBUNAL_COLUMN].nunique()),
        "year_min": int(dataframe[config.YEAR_COLUMN].min()),
        "year_max": int(dataframe[config.YEAR_COLUMN].max()),
        "target_column": config.TARGET_COLUMN,
        "digitalization_column": "procel1",
    }


def write_data_prep_note(scope_summary: dict[str, object], missingness: pd.DataFrame) -> None:
    top_missing = missingness.head(10).to_markdown(index=False)
    note = f"""# Data preparation note

## Scope

- Rows after filtering: {scope_summary['rows']}
- Branches: {', '.join(scope_summary['branches'])}
- Tribunals: {scope_summary['tribunals']}
- Period: {scope_summary['year_min']}-{scope_summary['year_max']}
- Target: `{scope_summary['target_column']}`
- Digitalization variable: `procel1`

## Data rules applied

1. Semicolon-delimited CNJ file loaded from the parent project data directory.
2. The pipeline tries `utf-8-sig` first and falls back to `latin-1` when decoding is inconsistent.
3. `nd` values converted to missing values.
4. Scope restricted to `Estadual`, `Federal`, and `Trabalho`.
5. Aggregate rows `TJ`, `TRF`, and `TRT` excluded.
6. Period restricted to 2015-2023.
7. Missing `dsc_tribunal` values filled with `sigla`.
8. Rows missing the main target were removed.

## Highest missingness columns

{top_missing}
"""
    save_markdown(note, config.TECHNICAL_NOTES_DIR / "data-preparation.md")


def write_variable_mapping_note() -> None:
    dictionary = load_variable_dictionary()
    selected = dictionary[dictionary["variable_name"].isin([config.TARGET_COLUMN, "procel1", "iad1", "cm1", "sajudmag1", "cn1", "g1", "h1"])]
    mapping_text = "# Variable mapping\n\n" + selected.sort_values("variable_name").to_markdown(index=False)
    save_markdown(mapping_text, config.METHODOLOGY_DIR / "variable-mapping.md")


def main() -> None:
    ensure_project_directories()
    modeling_dataset = build_modeling_dataset()
    missingness = build_missingness_table(modeling_dataset)
    scope_summary = build_scope_summary(modeling_dataset)

    save_csv(modeling_dataset, config.PROCESSED_DATA_DIR / "modeling_dataset.csv")
    save_csv(missingness, config.TABLES_DIR / "missingness_summary.csv")
    (config.PROCESSED_DATA_DIR / "dataset_scope.json").write_text(json.dumps(scope_summary, indent=2), encoding="utf-8")

    write_data_prep_note(scope_summary, missingness)
    write_variable_mapping_note()

    print(f"Saved modeling dataset with {scope_summary['rows']} rows.")


if __name__ == "__main__":
    main()
