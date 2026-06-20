from __future__ import annotations

from pathlib import Path

import pandas as pd

from . import config


def ensure_project_directories() -> None:
    directories = [
        config.RAW_DATA_DIR,
        config.PROCESSED_DATA_DIR,
        config.FIGURES_DIR,
        config.TABLES_DIR,
        config.MODELS_DIR,
        config.TECHNICAL_NOTES_DIR,
        config.ARTICLE_DRAFT_DIR,
        config.METHODOLOGY_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def read_semicolon_csv(path: Path, encoding: str = "latin-1") -> pd.DataFrame:
    encodings = ["utf-8-sig", encoding]

    for current_encoding in encodings:
        try:
            return pd.read_csv(path, sep=";", encoding=current_encoding, low_memory=False)
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError("codec", b"", 0, 1, f"Could not decode {path}")


def load_main_dataset() -> pd.DataFrame:
    return read_semicolon_csv(config.MAIN_DATASET_PATH)


def load_variable_dictionary() -> pd.DataFrame:
    dictionary = read_semicolon_csv(config.VARIABLE_DICTIONARY_PATH)
    dictionary.columns = ["variable_name", "description"]
    return dictionary


def replace_nd_with_missing(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe.replace("nd", pd.NA)


def coerce_numeric_columns(dataframe: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    converted = dataframe.copy()

    for column in columns:
        normalized = (
            converted[column]
            .astype("string")
            .str.strip()
            .str.replace(",", ".", regex=False)
        )
        converted[column] = pd.to_numeric(normalized, errors="coerce")

    return converted


def save_csv(dataframe: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(path, index=False)


def save_markdown(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def dataset_scope_mask(dataframe: pd.DataFrame) -> pd.Series:
    years = pd.to_numeric(dataframe[config.YEAR_COLUMN], errors="coerce")
    branches = dataframe[config.BRANCH_COLUMN].isin(config.SELECTED_BRANCHES)
    non_aggregate = ~dataframe[config.TRIBUNAL_COLUMN].isin(config.EXCLUDED_AGGREGATE_SIGLAS)
    valid_years = years.between(config.YEAR_START, config.YEAR_END)
    return branches & non_aggregate & valid_years
