# Modeling note

## Train-test split

- Train rows: 396
- Test rows: 106
- Train tribunals: 45
- Test tribunals: 12
- Split strategy: grouped holdout by `sigla`
- Tribunal overlap between train and test: `[]`

## Metrics

| model             |      r2 |     mae |    rmse |
|:------------------|--------:|--------:|--------:|
| random_forest     | 0.39527 | 216.421 | 334.287 |
| linear_regression | 0.28244 | 251.815 | 364.14  |

## Top linear coefficients

| feature                       |   coefficient |
|:------------------------------|--------------:|
| categorical__justica_Trabalho |    -701.99    |
| categorical__justica_Federal  |    -475.911   |
| numeric__h1                   |     173.799   |
| numeric__cn1                  |    -106.289   |
| numeric__iad1                 |     104.553   |
| numeric__sajudmag1            |     -88.1947  |
| numeric__procel1              |     -79.48    |
| numeric__cm1                  |      68.9714  |
| numeric__g1                   |      12.6065  |
| numeric__ano                  |      -6.10037 |

## Top random forest importances

| feature                       |   importance |
|:------------------------------|-------------:|
| categorical__justica_Trabalho |  0.315106    |
| numeric__h1                   |  0.187215    |
| numeric__g1                   |  0.183569    |
| numeric__iad1                 |  0.134385    |
| numeric__procel1              |  0.039792    |
| numeric__ano                  |  0.0381557   |
| numeric__sajudmag1            |  0.0345612   |
| numeric__cn1                  |  0.0340712   |
| numeric__cm1                  |  0.0327095   |
| categorical__justica_Federal  |  0.000436477 |

## Best random forest parameters

```json
{
  "model__max_depth": 10,
  "model__min_samples_split": 2,
  "model__n_estimators": 100
}
```
