from pathlib import Path
from langchain_community.llms import GPT4All
from langchain.prompts import ChatPromptTemplate, PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_community.vectorstores import Chroma
from langchain.schema.runnable import RunnablePassthrough
from langchain_community.embeddings.gpt4all import GPT4AllEmbeddings
from project_config import ProjectConfig

# Set filepaths and config variables.
PROJ_DIR = ProjectConfig.PROJ_DIR
MODELS_DIR = ProjectConfig.MODELS_DIR
DATA_PATH = ProjectConfig.DATA_PATH
VECTOR_PATH = ProjectConfig.VECTOR_PATH
EMBEDDER = ProjectConfig.EMBEDDER

# Fetch llm
chat_model = GPT4All(model=str(Path(MODELS_DIR / 'mistral-7b-openorca.gguf2.Q4_0.gguf')))

# Create system prompt to govern nature of llm responses.
sys_template_str = """Your name is AI. Your job is to answer questions about what food ingredients are in the pantry using the context provided below. Don't make up any information that's not from the context. If you don't know an answer, say you don't know.

{context}

{question}
"""
system_prompt = SystemMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=['context'], template=sys_template_str
    )
)

# Create humen prompt.
human_prompt = HumanMessagePromptTemplate(
    prompt=PromptTemplate(
        input_variables=['question'], template='{question}'
    )
)

# Combine system and humen message into beggining 
messages = [system_prompt, human_prompt]
chat_prompt = ChatPromptTemplate(
    input_variables=['context', 'question'],
    messages=messages,
)

# Load vector database and create context retriever for chain.
loaded_vector_db = Chroma(
    persist_directory=str(VECTOR_PATH),
    embedding_function=EMBEDDER,
)

retriever = loaded_vector_db.as_retriever()

# Create basic chain that uses retreived context in the prompt.
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | chat_prompt
    | chat_model
)