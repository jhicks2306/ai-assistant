
from pathlib import Path
from langchain_community.embeddings.gpt4all import GPT4AllEmbeddings

class ProjectConfig:
    PROJ_DIR = Path.cwd()
    MODELS_DIR = PROJ_DIR / 'models'
    DATA_PATH = PROJ_DIR / 'data' / 'pantry.txt'
    VECTOR_PATH = PROJ_DIR / "vector_db"
    EMBEDDER = GPT4AllEmbeddings()