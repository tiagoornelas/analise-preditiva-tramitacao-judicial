# Predictive analysis of judicial case duration

This repository contains the execution layer of the TCC study on predictive analysis of judicial tramitation time in Brazilian courts using official CNJ data.

## Study goal

Estimate first-degree tramitation time and quantify the role of judicial digitalization using tribunal-year aggregated data.

## Confirmed scope

- Main dataset: `../Base de Dados/JN_23-Set-2025.csv`
- Dictionary: `../Base de Dados/Variaveis_23-Set-2025.csv`
- Period: `2015-2023`
- Branches: `Estadual`, `Federal`, `Trabalho`
- Excluded aggregate rows: `TJ`, `TRF`, `TRT`
- Main target: `tpbaixc1m`
- Main digitalization variable: `procel1`

## Project structure

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── notebooks/
├── outputs/
├── reports/
└── src/
```

## Environment setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execution order

1. Prepare the filtered modeling dataset.
2. Generate exploratory summaries.
3. Train and evaluate the models.
4. Consolidate the interpretation notes.

### 1. Data preparation

```bash
python3 -m src.data_prep
```

### 2. Exploratory summaries

```bash
python3 -m src.exploratory
```

### 3. Modeling

```bash
python3 -m src.modeling
```

### 4. Evaluation summary

```bash
python3 -m src.evaluation
```

## Outputs

- `data/processed/modeling_dataset.csv`
- `outputs/tables/*.csv`
- `outputs/tables/model_metrics.csv`
- `reports/technical-notes/*.md`

## Notes

- The raw CNJ files in the parent project use semicolon separators.
- Encoding is inconsistent across files. The pipeline first attempts `utf-8-sig` for the main CNJ file and falls back to `latin-1` when needed.
- The project documents every methodological adjustment caused by the real available data.

## Smoke validation

```bash
.venv/bin/python -m src.validate_pipeline
```
