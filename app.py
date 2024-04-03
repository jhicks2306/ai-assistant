import streamlit as st
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from utils.load_data import create_vector_db
from routing import get_routing_chain
import json
import pantry_operations as po
from project_config import ProjectConfig

# Connect to pantry database
DB_PATH = ProjectConfig.DB_PATH
conn, cursor = po.connect_to_db(DB_PATH)

# Set up message history
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")
config = {"configurable": {"session_id": "any"}}

# Set up chain to route user messages to the correct response.
router = get_routing_chain()

# Placeholder function for querying with pantry.
def query_pantry(ingredients):
    return f'This is a pantry query?'

# Set up main chat model chain and pass message history.
model = Ollama(model='llama2')

prompt = ChatPromptTemplate.from_messages( 
    [
        ("system", "You are a helpful assistant called PantryPal."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ]
)

# Chain for when the response comes from the chat LLM.
chain = prompt | model
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="input",
    history_messages_key="history"
)

# Passthrough for when the response does not go through an LLM.
passthrough = RunnablePassthrough()
passthrough_with_history = RunnableWithMessageHistory(
    passthrough,
    lambda session_id: msgs,
    input_messages_key="input",
    history_messages_key="history"
)

# Define utility functions for streamed responses.
def chain_to_generator(input, chain):
    """Invoke chain as a stream."""
    return chain.stream({"input": input}, config)

def string_to_generator(input_string):
    """Convert string to stream of words."""
    for char in input_string:
        yield char

### The PANTRY ASSISTANT APP ###

st.title("Pantry Assistant")

# Render the chat history.
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# React to user input
if input := st.chat_input("What is up?"):
    # Display user input.
    st.chat_message("user").write(input)

    # Invoke router to direct the user input.
    route = router.invoke(input)
    fn_name = route.additional_kwargs['function_call']['name']
    fn_args = json.loads(route.additional_kwargs['function_call']['arguments'])

    # Run appropriate chain to generate response.
    if fn_name == 'add_ingredients':
        # Take response from SQL operation, add messages to history, and convert to stream.
        response = po.create_items(fn_args['ingredients'], conn=conn, cursor=cursor)
        msgs.add_user_message(input)
        msgs.add_ai_message(response)
        response = string_to_generator(response)
    elif fn_name == 'remove_ingredients':
        # Take response from SQL operation, add messages to history, and convert to stream.
        response = po.delete_items(fn_args['ingredients'], conn=conn, cursor=cursor)
        msgs.add_user_message(input)
        msgs.add_ai_message(response)
        response = string_to_generator(response)
    elif fn_name == 'query_pantry':
        response = chain_with_history.stream({"input": input}, config)

    # Write AI assistant response and add to message history.
    st.chat_message("assistant").write_stream(response)

    cursor.close()
    conn.close()
