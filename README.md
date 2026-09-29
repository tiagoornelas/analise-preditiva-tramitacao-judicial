# Análise Preditiva do Tempo de Tramitação Judicial

Estudo empírico sobre a duração dos processos no 1º grau da Justiça brasileira e o impacto da digitalização processual, utilizando dados consolidados do Conselho Nacional de Justiça (CNJ — Justiça em Números, 2015–2023).

---

## 1. Objetivo do Estudo

Quantificar a relação entre a digitalização judiciária (medida pelo índice de processos eletrônicos) e o tempo médio de tramitação de processos baixados no 1º grau, controlando por capacidade operacional, carga de trabalho por magistrado, demanda processual e variáveis socioeconômicas.

O estudo avalia a capacidade preditiva de modelos estatísticos e de aprendizado de máquina em dados agregados por tribunal-ano, com ênfase em generalização para tribunais não observados no treinamento.

---

## 2. Escopo Metodológico

- **Fonte de dados:** Relatório Justiça em Números (CNJ).
- **Período de análise:** 2015 a 2023.
- **Ramos abrangidos:** Estadual, Federal e Trabalho (57 tribunais, 502 observações tribunal-ano).
- **Tratamento de agregados:** Exclusão das linhas sintéticas de cúpula (`TJ`, `TRF`, `TRT`) para evitar redundância com as unidades jurisdicionais.
- **Variável-alvo (`target`):** `tpbaixc1m` — tempo médio de tramitação dos processos baixados no 1º grau (em dias).
- **Variável central de digitalização:** `procel1` — índice de processos eletrônicos no 1º grau.

### Variáveis Utilizadas

| Variável | Nome no CNJ | Descrição Técnica | Papel |
| :--- | :--- | :--- | :--- |
| `tpbaixc1m` | TpBaixC1 - Média | Tempo médio de tramitação das baixas no 1º grau (dias) | Variável-alvo |
| `procel1` | ProcEl1º | Índice de processos eletrônicos no 1º grau | Preditora (digitalização) |
| `iad1` | IAD1º | Processos baixados por caso novo no 1º grau | Preditora (vazão de demanda) |
| `cm1` | Cm1º | Casos novos por magistrado no 1º grau | Preditora (carga de trabalho) |
| `sajudmag1` | SajudMag1 | Servidores da área judiciária por magistrado no 1º grau | Preditora (apoio técnico) |
| `cn1` | Cn1º | Casos novos no 1º grau | Preditora (escala do tribunal) |
| `h1` | h1 | População residente sob jurisdição | Preditora (demográfica) |
| `g1` | G1 | Despesa total da Justiça em relação ao PIB | Preditora (recurso econômico) |
| `ano` | ano | Ano de referência da observação | Preditora (tendência temporal) |
| `justica` | justica | Ramo de justiça (`Estadual`, `Federal`, `Trabalho`) | Preditora categórica |

---

## 3. Validação e Controle de Vazamento de Dados

A divisão entre treino e teste adotou estratégia estrita de **Grouped Holdout por tribunal** (`GroupShuffleSplit` por `sigla`), separando 80% dos tribunais para treino e 20% para teste (`random_state=42`):

- **Treino:** 396 observações distribuídas em 45 tribunais.
- **Teste:** 106 observações distribuídas em 12 tribunais.
- **Sobreposição institucional:** Nula (`overlap = []`).

```text
Divisão Estruturada por Grupo (Tribunais):
┌──────────────────────────────┬──────────────────────────────┐
│ Treino (45 Tribunais)        │ Teste (12 Tribunais)         │
│ 396 observações (2015-2023)  │ 106 observações (2015-2023)  │
└──────────────────────────────┴──────────────────────────────┘
  * Nenhum tribunal presente no teste foi exposto ao treinamento.
```

### Interpretação do $R^2 \approx 0,40$

O modelo Random Forest obteve $R^2 \approx 0,395$ no conjunto de teste:

1. **Rigor empírico:** O particionamento em nível de tribunal exige que o modelo generalize para organizações públicas com perfis de governança e litigiosidade nunca vistos durante o ajuste.
2. **Escopo dos dados macroeconômicos:** Em dados agregados tribunal-ano, $40\%$ da variância temporal e interinstitucional do tempo de tramitação decorre de escala, digitalização, força de trabalho e ramo.
3. **Ausência de overfitting artificial:** Modelos avaliados por amostragem aleatória simples (sem agrupamento) apresentam métricas artificialmente elevadas por memorização da autocorrelação intrínseca de cada tribunal. O split agrupado reflete o desempenho real do modelo diante de novos tribunais.

---

## 4. Resultados da Modelagem

### Comparação de Desempenho

| Modelo | $R^2$ | MAE (dias) | RMSE (dias) |
| :--- | :---: | :---: | :---: |
| **Random Forest Regressor** | **0,4006** | **215,89** | **332,81** |
| Regressão Linear (Baseline) | 0,2824 | 251,81 | 364,14 |

### Importância das Variáveis (Random Forest)

| Feature | Importância Relativa | Descrição |
| :--- | :---: | :--- |
| `categorical__justica_Trabalho` | 0,3151 | Diferencial estrutural da Justiça do Trabalho |
| `numeric__h1` | 0,1873 | População jurisdicionada |
| `numeric__g1` | 0,1835 | Despesa em relação ao PIB |
| `numeric__iad1` | 0,1318 | Vazão de processos baixados por caso novo |
| `numeric__procel1` | 0,0398 | Índice de processos eletrônicos no 1º grau |
| `numeric__ano` | 0,0380 | Efeito fixo temporal |
| `numeric__cn1` | 0,0367 | Volume absoluto de novas demandas |
| `numeric__sajudmag1` | 0,0345 | Apoio funcional por magistrado |
| `numeric__cm1` | 0,0329 | Carga de processos novos por magistrado |
| `categorical__justica_Federal` | 0,0004 | Diferencial específico da Justiça Federal |

### Coeficientes da Regressão Linear Padronizada

| Feature | Coeficiente | Interpretação |
| :--- | :---: | :--- |
| `categorical__justica_Trabalho` | -701,99 | Menor tempo médio de tramitação frente à Estadual |
| `categorical__justica_Federal` | -475,91 | Menor tempo médio de tramitação frente à Estadual |
| `numeric__h1` | +173,80 | Tribunais com maior população associados a maior tempo |
| `numeric__cn1` | -106,29 | Efeito conjunto com escala do tribunal |
| `numeric__iad1` | +104,55 | Ajuste de vazão e acúmulo de estoque |
| `numeric__sajudmag1` | -88,19 | Maior número de servidores reduz o tempo médio |
| `numeric__procel1` | -79,48 | Aumento na digitalização associado à redução do tempo |
| `numeric__cm1` | +68,97 | Sobrecarga de casos novos por magistrado eleva o tempo |
| `numeric__g1` | +12,61 | Despesa em relação ao PIB |
| `numeric__ano` | -6,10 | Tendência histórica secular de redução do tempo |

---

## 5. Panorama Descritivo

### Síntese por Ramo de Justiça

| Ramo | Observações | Média de Duração (dias) | Mediana (dias) | Média Digitalização (`procel1`) | Média `iad1` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Estadual | 240 | 996,15 | 959,22 | 81,15% | 1,07 |
| Federal | 46 | 834,31 | 671,88 | 84,65% | 1,00 |
| Trabalho | 216 | 379,64 | 345,50 | 98,64% | 1,11 |

### Evolução Temporal (2015–2023)

| Ano | Tribunais | Média Duração (dias) | Digitalização Média | Média Casos Novos |
| :---: | :---: | :---: | :---: | :---: |
| 2015 | 52 | 679,87 | 63,74% | 279.191 |
| 2016 | 56 | 705,36 | 75,96% | 285.706 |
| 2017 | 56 | 888,87 | 82,69% | 294.227 |
| 2018 | 56 | 782,35 | 89,21% | 275.402 |
| 2019 | 56 | 790,15 | 90,72% | 284.363 |
| 2020 | 56 | 652,85 | 97,84% | 257.432 |
| 2021 | 56 | 668,55 | 99,14% | 292.486 |
| 2022 | 57 | 664,00 | 99,62% | 327.869 |
| 2023 | 57 | 612,63 | 99,85% | 356.257 |

---

## 6. Estrutura do Repositório

```text
.
├── data/
│   ├── raw/                       # Armazenamento de dados brutos
│   └── processed/                 # Dataset consolidado para modelagem
├── docs/
│   └── methodology/               # Mapeamento de variáveis e notas metodológicas
├── notebooks/                     # Cadernos de exploração e modelagem
├── outputs/
│   ├── figures/                   # Gráficos exportados
│   ├── models/                    # Parâmetros e artefatos de modelos
│   └── tables/                    # Tabelas analíticas geradas pelo pipeline
├── reports/
│   ├── article-draft/             # Rascunho estruturado do artigo científico
│   └── technical-notes/           # Notas técnicas detalhadas de cada etapa
└── src/                           # Código modular do pipeline de análise
    ├── config.py                  # Configurações globais e caminhos
    ├── data_prep.py               # Ingestão, limpeza e filtragem dos dados
    ├── exploratory.py             # Estatísticas descritivas e matrizes
    ├── modeling.py                # Treinamento com GroupShuffleSplit e métricas
    ├── evaluation.py              # Consolidação dos resultados analíticos
    ├── utils.py                   # Funções utilitárias de I/O
    └── validate_pipeline.py       # Validação e testes automatizados do pipeline
```

---

## 7. Instruções de Execução

### Configuração do Ambiente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Execução do Pipeline

Os módulos do pipeline devem ser executados na ordem abaixo:

1. **Preparação dos Dados:**
   ```bash
   python3 -m src.data_prep
   ```

2. **Sumários Exploratórios:**
   ```bash
   python3 -m src.exploratory
   ```

3. **Treinamento e Validação dos Modelos:**
   ```bash
   python3 -m src.modeling
   ```

4. **Consolidação dos Resultados:**
   ```bash
   python3 -m src.evaluation
   ```

### Teste e Validação Automatizada

Para validar a integridade de todas as etapas e dos artefatos produzidos:

```bash
python3 -m src.validate_pipeline
```

---

## 8. Documentação Técnica e Artigo

- **Rascunho do Artigo Científico:** [reports/article-draft/artigo-cientifico.md](reports/article-draft/artigo-cientifico.md)
- **Log de Decisões Metodológicas:** [reports/technical-notes/decisions-log.md](reports/technical-notes/decisions-log.md)
- **Resultados de Modelagem:** [reports/technical-notes/modeling-results.md](reports/technical-notes/modeling-results.md)
- **Mapeamento de Variáveis:** [docs/methodology/variable-mapping.md](docs/methodology/variable-mapping.md)
- **Tabelas Consolidadas:** [outputs/tables/](outputs/tables/)
