# Evaluation summary

## Best current model

- Model: `random_forest`
- R2: `0.4006`
- MAE: `215.8855`
- RMSE: `332.8133`

## Top random forest features

| feature                       |   importance |
|:------------------------------|-------------:|
| categorical__justica_Trabalho |  0.315106    |
| numeric__h1                   |  0.187315    |
| numeric__g1                   |  0.183504    |
| numeric__iad1                 |  0.131754    |
| numeric__procel1              |  0.0397977   |
| numeric__ano                  |  0.0380122   |
| numeric__cn1                  |  0.036735    |
| numeric__sajudmag1            |  0.0344618   |
| numeric__cm1                  |  0.0329306   |
| categorical__justica_Federal  |  0.000384738 |

## Interpretation checklist

1. Check where `procel1` appears in the random forest ranking.
2. Compare the sign of the linear effect for digitalization.
3. Confirm whether branch effects remain relevant after controlling for structural variables.
4. Use the saved tables to draft the results and discussion sections of the article.
