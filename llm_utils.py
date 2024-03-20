from pathlib import Path
import re
from langchain_community.llms import GPT4All
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import LLMChain
from llama_index.core import Settings
from llama_index.embeddings.langchain import LangchainEmbedding
from llama_index.core.indices.prompt_helper import PromptHelper
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core import StorageContext, load_index_from_storage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# Set filepaths
proj_dir = Path.cwd()
models_dir = proj_dir / 'models'
data_dir = proj_dir / 'data'

def get_default_settings():
    # Load the model
    llm = GPT4All(model=str(Path(models_dir / 'mistral-7b-openorca.gguf2.Q4_0.gguf')))

    # SentenceSplitter used to split our data into multiple chunks
    # Only a number of relevant chunks will be retrieved and fed into LLMs
    node_parser = SentenceSplitter(chunk_size=300, chunk_overlap=20)

    # An embedding model used to structure text into representations.
    embed_model = LangchainEmbedding(
        HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    )

    # PromptHelper can help deal with LLM context window and token limitations
    prompt_helper = PromptHelper(context_window=2048)

    return llm, embed_model, prompt_helper, node_parser
    
def create_index(path_to_data, path_to_cache=None):
    if isinstance(path_to_data, Path): path_to_data = str(path_to_data)

    # Load data.txt into a document
    documents = SimpleDirectoryReader(input_files=[path_to_data]).load_data()

    # Process data (chunking, embedding, indexing).
    index = VectorStoreIndex.from_documents(documents)

    if path_to_cache is not None:
        # Save the index to save time next time.
        if isinstance(path_to_cache, Path): path_to_cache = str(path_to_cache)
        index.storage_context.persist(persist_dir=path_to_cache)

    return index

def check_for_cached_index():
    pass

def query_index(index=None, query=None):
    query_engine = index.as_query_engine()
    return query_engine.query(query)



def extract_ingredients_from_text(text, llm):
    """Use a fixed custom template to extract a list of ingredients."""
    prompt = PromptTemplate.from_template('Provide a comma separated list of the food ingredients mentioned in the following quoted text: "{text}"')
    chain = LLMChain(llm=llm, prompt=prompt)
    output = chain.run(text=text)
    return output

def clean_string(input_string):
    # Remove whitespace characters except spaces
    cleaned_string = re.sub(r'[^\S\n]', '', input_string)
    # Remove all punctuation except commas
    cleaned_string = re.sub(r'[^\w\s,]', '', cleaned_string)
    return cleaned_string








