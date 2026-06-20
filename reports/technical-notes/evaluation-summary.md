# Evaluation summary

## Best current model

- Model: `random_forest`
- R2: `0.3953`
- MAE: `216.4214`
- RMSE: `334.2874`

## Top random forest features

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

## Interpretation checklist

1. Check where `procel1` appears in the random forest ranking.
2. Compare the sign of the linear effect for digitalization.
3. Confirm whether branch effects remain relevant after controlling for structural variables.
4. Use the saved tables to draft the results and discussion sections of the article.
