# Data preparation note

## Scope

- Rows after filtering: 502
- Branches: Estadual, Federal, Trabalho
- Tribunals: 57
- Period: 2015-2023
- Target: `tpbaixc1m`
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

| column       |   missing_count |   missing_ratio |
|:-------------|----------------:|----------------:|
| ano          |               0 |               0 |
| cm1          |               0 |               0 |
| cn1          |               0 |               0 |
| dsc_tribunal |               0 |               0 |
| g1           |               0 |               0 |
| h1           |               0 |               0 |
| iad1         |               0 |               0 |
| justica      |               0 |               0 |
| procel1      |               0 |               0 |
| sajudmag1    |               0 |               0 |
