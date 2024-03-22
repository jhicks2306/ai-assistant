from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.gpt4all import GPT4AllEmbeddings
from langchain_community.document_loaders.text import TextLoader
from project_config import ProjectConfig

# Set filepaths and config variables.
PROJ_DIR = ProjectConfig.PROJ_DIR
MODELS_DIR = ProjectConfig.MODELS_DIR
DATA_PATH = ProjectConfig.DATA_PATH
VECTOR_PATH = ProjectConfig.VECTOR_PATH
EMBEDDER = ProjectConfig.EMBEDDER

def create_vector_db():
    # Load text into Documents objects.
    loader = TextLoader(file_path=str(DATA_PATH))
    documents = loader.load()

    # TODO: May need text splitter here.

    # Create vector database.
    vector_db = Chroma.from_documents(
        documents=documents, embedding=EMBEDDER, persist_directory=str(VECTOR_PATH)
    )

if __name__ == "__main__":
    create_vector_db()