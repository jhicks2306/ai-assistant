from pathlib import Path
from langchain_community.llms import GPT4All
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough
from project_config import ProjectConfig

# Set filepaths and config variables.
PROJ_DIR = ProjectConfig.PROJ_DIR
MODELS_DIR = ProjectConfig.MODELS_DIR
DATA_PATH = ProjectConfig.DATA_PATH
VECTOR_PATH = ProjectConfig.VECTOR_PATH
EMBEDDER = ProjectConfig.EMBEDDER

def get_pantry_query_chain():
    # Fetch llm
    model = GPT4All(model=str(Path(MODELS_DIR / 'mistral-7b-openorca.gguf2.Q4_0.gguf')))

    # Create prompt to govern nature of llm responses.
    template_str = """Your job is to answer questions about what food ingredients are in the pantry, using the information provided below. Don't make up any information that's not provided. If you don't know an answer, say you don't know.

    {context}

    {question}
    """

    prompt = PromptTemplate.from_template(template_str)

    # Load vector database and create context retriever for chain.
    loaded_vector_db = Chroma(
        persist_directory=str(VECTOR_PATH),
        embedding_function=EMBEDDER,
    )

    retriever = loaded_vector_db.as_retriever(search_kwargs={"k": 1}) # TODO change k when db gets bigger.

    # Create basic chain that uses retreived context in the prompt.
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
    )

    return chain