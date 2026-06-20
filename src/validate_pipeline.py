from __future__ import annotations

import pandas as pd

from . import config
from .data_prep import build_modeling_dataset
from .modeling import run_modeling, split_dataset
from .utils import ensure_project_directories, load_main_dataset


def assert_required_columns(dataframe: pd.DataFrame) -> None:
    required_columns = {
        config.YEAR_COLUMN,
        config.BRANCH_COLUMN,
        config.TRIBUNAL_COLUMN,
        config.TARGET_COLUMN,
        "procel1",
        "iad1",
        "cm1",
        "sajudmag1",
        "cn1",
        "g1",
        "h1",
        "dsc_tribunal",
    }
    missing_columns = sorted(required_columns - set(dataframe.columns))
    if missing_columns:
        raise AssertionError(f"Missing required columns: {missing_columns}")


def assert_scope_rules(dataframe: pd.DataFrame) -> None:
    branches = set(dataframe[config.BRANCH_COLUMN].unique())
    if branches != set(config.SELECTED_BRANCHES):
        raise AssertionError(f"Unexpected branches in modeling dataset: {sorted(branches)}")

    years = dataframe[config.YEAR_COLUMN]
    if int(years.min()) != config.YEAR_START or int(years.max()) != config.YEAR_END:
        raise AssertionError("Unexpected year bounds in modeling dataset")

    if dataframe[config.TRIBUNAL_COLUMN].isin(config.EXCLUDED_AGGREGATE_SIGLAS).any():
        raise AssertionError("Aggregate branch rows were not fully excluded")


def assert_no_missing_target(dataframe: pd.DataFrame) -> None:
    if dataframe[config.TARGET_COLUMN].isna().any():
        raise AssertionError("Target column still contains missing values")


def assert_modeling_runs() -> None:
    results = run_modeling()
    metrics = results["metrics"]
    if metrics.empty:
        raise AssertionError("Model metrics were not produced")

    if results["group_overlap"]:
        raise AssertionError(f"Grouped split leaked tribunals across train/test: {results['group_overlap']}")


def assert_disjoint_group_split(dataframe: pd.DataFrame) -> None:
    _, _, _, _, train_groups, test_groups = split_dataset(dataframe)
    overlap = set(train_groups.tolist()) & set(test_groups.tolist())
    if overlap:
        raise AssertionError(f"Train/test tribunal overlap detected: {sorted(overlap)}")


def main() -> None:
    ensure_project_directories()
    raw = load_main_dataset()
    assert_required_columns(raw)

    modeling_dataset = build_modeling_dataset()
    assert_scope_rules(modeling_dataset)
    assert_no_missing_target(modeling_dataset)
    assert_disjoint_group_split(modeling_dataset)
    assert_modeling_runs()

    print("Pipeline validation passed.")


if __name__ == "__main__":
    main()
