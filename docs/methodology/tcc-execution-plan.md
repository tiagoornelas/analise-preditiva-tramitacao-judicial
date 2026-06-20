# TCC execution plan

## Objective

Execute the empirical study proposed in the approved pre-project with maximum adherence to the real CNJ data available in this repository, then use the results to support the final scientific article.

## Confirmed analytical scope

- Main dataset: `Base de Dados/JN_23-Set-2025.csv`
- Variable dictionary: `Base de Dados/Variaveis_23-Set-2025.csv`
- Time window: `2015-2023`
- Branches: `Estadual`, `Federal`, `Trabalho`
- Aggregate branch rows excluded: `TJ`, `TRF`, `TRT`
- Main target: `tpbaixc1m`
- Main digitalization predictor: `procel1`
- Modeling strategy: `Linear Regression` baseline and `Random Forest` main model
- Technical stack: Python scripts with supporting notebooks

## Working phases

1. Create the private project repository structure.
2. Prepare a reproducible data ingestion and cleaning pipeline.
3. Build the modeling dataset using validated CNJ variables.
4. Produce exploratory tables and descriptive evidence.
5. Train and compare baseline and main predictive models.
6. Consolidate findings about digitalization and tramitation time.
7. Draft the final scientific article in Markdown using the approved pre-project as structure reference.

## Expected deliverables

1. Reproducible Python code.
2. Processed modeling dataset.
3. Exploratory summaries and output tables.
4. Model comparison metrics.
5. Methodological notes documenting every deviation from the original pre-project wording.
6. Final article draft in Markdown.

## Key methodological decisions

### Why `tpbaixc1m`

The original pre-project names `tpbaix1m`, but the available CNJ file does not expose that exact field. The current implementation therefore uses `tpbaixc1m` as the target because it is the closest usable proxy with strong coverage in the filtered sample.

### Why `procel1`

`procel1` is the operational CNJ field that best represents the first-degree electronic process index, which is the substantive digitalization construct promised in the pre-project.

### Why scripts plus notebooks

Scripts will hold the reproducible pipeline. Notebooks will support guided inspection, interpretation, and article writing.

## Repository name

- `analise-preditiva-tramitacao-judicial`
