import os
import threading
from pathlib import Path
from llama_index.core import Settings
from llama_index.core import StorageContext, load_index_from_storage
from llm_utils import get_default_settings, create_index, query_index, extract_ingredients_from_text, clean_string
from text2speech import text2speech
from speech2text import listen, speech2text

def llm_query():
    # Capture user query.
    audio = listen()
    user_query = speech2text(audio)

    if 'no thank you' in user_query.lower():
        return False

    # Play holding response whilst waiting for actual reponse from llm.
    thread = threading.Thread(target=text2speech, args=("One moment. Let me check for you.",))
    thread.start()
    response = query_index(index, user_query)
    thread.join()

    # Print and play llm response.
    response_text = response.response
    print('Answer: ', response_text)
    text2speech(response_text)
    return True


if __name__ == "__main__":

    # Apply default settings for llama-index
    llm, embed_model, prompt_helper, node_parser = get_default_settings()
    Settings.llm = llm
    Settings.embed_model = embed_model
    Settings.prompt_helper = prompt_helper
    Settings.node_parser = node_parser

    # Set filepaths
    proj_dir = Path.cwd()
    models_dir = proj_dir / 'models'
    data_dir = proj_dir / 'data'
    path_to_data = data_dir / 'pantry.txt'
    path_to_cache = proj_dir / 'cache'


    # Get or create index.
    if os.listdir(path_to_cache) != 0:
        # If cache contains files then use it.
        storage_context = StorageContext.from_defaults(persist_dir=path_to_cache)
        index = load_index_from_storage(storage_context)
    else:
        index = create_index(path_to_data, path_to_cache)

    text2speech("Hi James, how can I help?")

    llm_query()

    loop = True
    while loop:
        text2speech("Anything else I can help you with?")
        loop = llm_query() 

    text2speech("Ok, speak soon!")