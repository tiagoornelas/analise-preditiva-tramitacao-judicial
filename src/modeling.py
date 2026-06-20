from __future__ import annotations

import json

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, GroupKFold, GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression

from . import config
from .utils import ensure_project_directories, save_csv, save_markdown


def load_modeling_dataset() -> pd.DataFrame:
    return pd.read_csv(config.PROCESSED_DATA_DIR / "modeling_dataset.csv")


def feature_columns() -> list[str]:
    return config.NUMERIC_FEATURES + config.CATEGORICAL_FEATURES


def split_dataset(dataframe: pd.DataFrame):
    features = dataframe[feature_columns()]
    target = dataframe[config.TARGET_COLUMN]
    groups = dataframe[config.TRIBUNAL_COLUMN]
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=config.RANDOM_STATE)
    train_indices, test_indices = next(splitter.split(features, target, groups=groups))

    return (
        features.iloc[train_indices].reset_index(drop=True),
        features.iloc[test_indices].reset_index(drop=True),
        target.iloc[train_indices].reset_index(drop=True),
        target.iloc[test_indices].reset_index(drop=True),
        groups.iloc[train_indices].reset_index(drop=True),
        groups.iloc[test_indices].reset_index(drop=True),
    )


def build_linear_pipeline() -> Pipeline:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", drop="first", sparse_output=False)),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, config.NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, config.CATEGORICAL_FEATURES),
        ]
    )

    return Pipeline(steps=[("preprocessor", preprocessor), ("model", LinearRegression())])


def build_random_forest_pipeline() -> Pipeline:
    numeric_pipeline = Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))])
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", drop="first", sparse_output=False)),
        ]
    )
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, config.NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, config.CATEGORICAL_FEATURES),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", RandomForestRegressor(random_state=config.RANDOM_STATE, n_jobs=-1)),
        ]
    )


def regression_metrics(name: str, actual, predicted) -> dict[str, float | str]:
    rmse = float(np.sqrt(mean_squared_error(actual, predicted)))
    return {
        "model": name,
        "r2": r2_score(actual, predicted),
        "mae": mean_absolute_error(actual, predicted),
        "rmse": rmse,
    }


def extract_feature_names(pipeline: Pipeline) -> list[str]:
    preprocessor = pipeline.named_steps["preprocessor"]
    return list(preprocessor.get_feature_names_out())


def linear_feature_effects(pipeline: Pipeline) -> pd.DataFrame:
    model = pipeline.named_steps["model"]
    features = extract_feature_names(pipeline)
    return pd.DataFrame({"feature": features, "coefficient": model.coef_}).sort_values("coefficient", key=lambda series: series.abs(), ascending=False)


def forest_feature_importance(pipeline: Pipeline) -> pd.DataFrame:
    model = pipeline.named_steps["model"]
    features = extract_feature_names(pipeline)
    return pd.DataFrame({"feature": features, "importance": model.feature_importances_}).sort_values("importance", ascending=False)


def run_modeling() -> dict[str, object]:
    dataframe = load_modeling_dataset()
    x_train, x_test, y_train, y_test, train_groups, test_groups = split_dataset(dataframe)

    linear_pipeline = build_linear_pipeline()
    linear_pipeline.fit(x_train, y_train)
    linear_predictions = linear_pipeline.predict(x_test)
    linear_metrics = regression_metrics("linear_regression", y_test, linear_predictions)

    random_forest_pipeline = build_random_forest_pipeline()
    grid = GridSearchCV(
        estimator=random_forest_pipeline,
        param_grid={
            "model__n_estimators": [100, 200],
            "model__max_depth": [None, 10, 20],
            "model__min_samples_split": [2, 5],
        },
        cv=GroupKFold(n_splits=3),
        scoring="r2",
        n_jobs=-1,
    )
    grid.fit(x_train, y_train, groups=train_groups)
    best_forest_pipeline = grid.best_estimator_
    forest_predictions = best_forest_pipeline.predict(x_test)
    forest_metrics = regression_metrics("random_forest", y_test, forest_predictions)

    train_group_set = set(train_groups.tolist())
    test_group_set = set(test_groups.tolist())

    return {
        "metrics": pd.DataFrame([linear_metrics, forest_metrics]).sort_values("r2", ascending=False),
        "linear_effects": linear_feature_effects(linear_pipeline),
        "forest_importance": forest_feature_importance(best_forest_pipeline),
        "best_forest_params": grid.best_params_,
        "test_rows": int(len(y_test)),
        "train_rows": int(len(y_train)),
        "train_groups": int(len(train_group_set)),
        "test_groups": int(len(test_group_set)),
        "group_overlap": sorted(train_group_set & test_group_set),
    }


def write_modeling_note(results: dict[str, object]) -> None:
    metrics = results["metrics"].to_markdown(index=False)
    top_linear = results["linear_effects"].head(10).to_markdown(index=False)
    top_forest = results["forest_importance"].head(10).to_markdown(index=False)
    best_params = json.dumps(results["best_forest_params"], indent=2)

    note = f"""# Modeling note

## Train-test split

- Train rows: {results['train_rows']}
- Test rows: {results['test_rows']}
- Train tribunals: {results['train_groups']}
- Test tribunals: {results['test_groups']}
- Split strategy: grouped holdout by `{config.TRIBUNAL_COLUMN}`
- Tribunal overlap between train and test: `{results['group_overlap']}`

## Metrics

{metrics}

## Top linear coefficients

{top_linear}

## Top random forest importances

{top_forest}

## Best random forest parameters

```json
{best_params}
```
"""
    save_markdown(note, config.TECHNICAL_NOTES_DIR / "modeling-results.md")


def main() -> None:
    ensure_project_directories()
    results = run_modeling()

    save_csv(results["metrics"], config.TABLES_DIR / "model_metrics.csv")
    save_csv(results["linear_effects"], config.TABLES_DIR / "linear_feature_effects.csv")
    save_csv(results["forest_importance"], config.TABLES_DIR / "random_forest_feature_importance.csv")
    (config.MODELS_DIR / "random_forest_best_params.json").write_text(json.dumps(results["best_forest_params"], indent=2), encoding="utf-8")

    write_modeling_note(results)
    print("Saved modeling outputs.")


if __name__ == "__main__":
    main()
