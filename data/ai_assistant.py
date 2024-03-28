import threading
from pantry_query import get_pantry_query_chain
from text2speech import text2speech
from speech2text import listen, speech2text
from project_config import ProjectConfig

PROJ_DIR = ProjectConfig.PROJ_DIR
MODELS_DIR = ProjectConfig.MODELS_DIR
DATA_PATH = ProjectConfig.DATA_PATH
VECTOR_PATH = ProjectConfig.VECTOR_PATH
EMBEDDER = ProjectConfig.EMBEDDER

def llm_query():
    # Capture user query.
    audio = listen()
    user_query = speech2text(audio)

    if 'no thank you' in user_query.lower():
        return False

    # Play holding response whilst waiting for actual reponse from llm.
    thread = threading.Thread(target=text2speech, args=("One moment. Let me check for you.",))
    thread.start()
    response_text = chain.invoke(user_query)
    thread.join()

    # Print and play llm response.
    print('Answer: ', response_text)
    text2speech(response_text)
    return True

if __name__ == "__main__":

    chain = get_pantry_query_chain()

    text2speech("Hi James, how can I help?")

    llm_query()

    loop = True
    while loop:
        text2speech("Anything else I can help you with?")
        loop = llm_query() 

    text2speech("Ok, speak soon!")