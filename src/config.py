from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"
MODELS_DIR = OUTPUTS_DIR / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
TECHNICAL_NOTES_DIR = REPORTS_DIR / "technical-notes"
ARTICLE_DRAFT_DIR = REPORTS_DIR / "article-draft"
DOCS_DIR = PROJECT_ROOT / "docs"
METHODOLOGY_DIR = DOCS_DIR / "methodology"

SOURCE_ROOT = PROJECT_ROOT.parent
SOURCE_DATA_DIR = SOURCE_ROOT / "Base de Dados"
MAIN_DATASET_PATH = SOURCE_DATA_DIR / "JN_23-Set-2025.csv"
VARIABLE_DICTIONARY_PATH = SOURCE_DATA_DIR / "Variaveis_23-Set-2025.csv"

TARGET_COLUMN = "tpbaixc1m"
BRANCH_COLUMN = "justica"
TRIBUNAL_COLUMN = "sigla"
YEAR_COLUMN = "ano"

SELECTED_BRANCHES = ["Estadual", "Federal", "Trabalho"]
EXCLUDED_AGGREGATE_SIGLAS = ["TJ", "TRF", "TRT"]
YEAR_START = 2015
YEAR_END = 2023

NUMERIC_FEATURES = [
    "procel1",
    "iad1",
    "cm1",
    "sajudmag1",
    "cn1",
    "h1",
    "g1",
    YEAR_COLUMN,
]

CATEGORICAL_FEATURES = [BRANCH_COLUMN]

MODEL_COLUMNS = [
    YEAR_COLUMN,
    BRANCH_COLUMN,
    TRIBUNAL_COLUMN,
    "dsc_tribunal",
    TARGET_COLUMN,
    "g1",
    "h1",
    "procel1",
    "iad1",
    "cm1",
    "sajudmag1",
    "cn1",
]

RANDOM_STATE = 42
