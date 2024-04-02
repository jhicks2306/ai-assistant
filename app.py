import streamlit as st
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
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

# Set up chain to route user messages to the correct response.
router = get_routing_chain()


# Placeholder function for querying with pantry.
def query_pantry(ingredients):
    return f'Ingredients added: {ingredients}'


# Set up main chat model chain and pass message history.
model = Ollama(model='llama2')

prompt = ChatPromptTemplate.from_messages( 
    [
        ("system", "You are a helpful assistant called PantryPal."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ]
)

chain = prompt | model
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="question",
    history_messages_key="history"
)

# Define utility function for streamed responses.
def response_generator(prompt):
    """Function to invoke chain as a stream."""
    config = {"configurable": {"session_id": "any"}}
    return chain_with_history.stream({"question": prompt}, config)

### The PANTRY ASSISTANT APP ###

st.title("Pantry Assistant")

# Render the chat history.
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user input (saved automatically in chat history)
    st.chat_message("user").write(prompt)

    route = router.invoke(prompt)
    fn_name = route.additional_kwargs['function_call']['name']
    fn_args = json.loads(route.additional_kwargs['function_call']['arguments'])

    if fn_name == 'add_ingredients':
        response = po.create_items(fn_args['ingredients'], conn=conn, cursor=cursor)
    elif fn_name == 'remove_ingredients':
        response = po.delete_items(fn_args['ingredients'], conn=conn, cursor=cursor)
    elif fn_name == 'query_pantry':
        response = query_pantry(fn_args['ingredients'])

    st.chat_message("assistant").write(response)

    # # Invoke chain for response.
    # response_stream = response_generator(prompt)
    # # Write AI response.
    # st.chat_message("assistant").write_stream(response_stream)

    cursor.close()
    conn.close()
