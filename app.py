import streamlit as st
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from utils.load_data import create_vector_db
from pantry_query import get_pantry_query_chain

# Set up message history
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

view_messages = st.expander("View the message contents in session state.")

# Set up LangChain and pass message history.
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

# chain = get_pantry_query_chain()

def response_generator(prompt):
    # Funcion to invoke chain as a stream.
    config = {"configurable": {"session_id": "any"}}
    return chain_with_history.stream({"question": prompt}, config)

st.title("Pantry Assistant")

# Render the chat history.
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user input (saved automatically in chat history)
    st.chat_message("user").write(prompt)
    # Invoke chain for response.
    response_stream = response_generator(prompt)
    # Write AI response.
    st.chat_message("assistant").write_stream(response_stream)
