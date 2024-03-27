
from pathlib import Path
from langchain_community.embeddings import OllamaEmbeddings

class ProjectConfig:
    PROJ_DIR = Path.cwd()
    MODELS_DIR = PROJ_DIR / 'models'
    DATA_PATH = PROJ_DIR / 'data' / 'pantry.txt'
    DB_PATH = PROJ_DIR / 'pantry.db'
    VECTOR_PATH = PROJ_DIR / "vector_db"
    EMBEDDER = OllamaEmbeddings()