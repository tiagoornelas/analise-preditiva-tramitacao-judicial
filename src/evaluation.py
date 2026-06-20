from __future__ import annotations

import pandas as pd

from . import config
from .utils import ensure_project_directories, save_markdown


def load_metrics() -> pd.DataFrame:
    return pd.read_csv(config.TABLES_DIR / "model_metrics.csv")


def load_feature_importance() -> pd.DataFrame:
    return pd.read_csv(config.TABLES_DIR / "random_forest_feature_importance.csv")


def write_evaluation_summary(metrics: pd.DataFrame, importance: pd.DataFrame) -> None:
    best_model = metrics.sort_values("r2", ascending=False).iloc[0]
    top_features = importance.head(10).to_markdown(index=False)

    summary = f"""# Evaluation summary

## Best current model

- Model: `{best_model['model']}`
- R2: `{best_model['r2']:.4f}`
- MAE: `{best_model['mae']:.4f}`
- RMSE: `{best_model['rmse']:.4f}`

## Top random forest features

{top_features}

## Interpretation checklist

1. Check where `procel1` appears in the random forest ranking.
2. Compare the sign of the linear effect for digitalization.
3. Confirm whether branch effects remain relevant after controlling for structural variables.
4. Use the saved tables to draft the results and discussion sections of the article.
"""
    save_markdown(summary, config.TECHNICAL_NOTES_DIR / "evaluation-summary.md")


def main() -> None:
    ensure_project_directories()
    metrics = load_metrics()
    importance = load_feature_importance()
    write_evaluation_summary(metrics, importance)
    print("Saved evaluation summary.")


if __name__ == "__main__":
    main()
