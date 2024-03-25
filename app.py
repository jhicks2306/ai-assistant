import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from load_data import create_vector_db
from pantry_query import get_pantry_query_chain

if "model" not in st.session_state:
    st.session_state["model"] = 'llama2'

chain = get_pantry_query_chain()

# Streamed response emulator
def response_generator(prompt):
    return chain.stream(prompt)

st.title("Pantry Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat mesages from history on app rerun.
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container.
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history.
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(prompt))

    # Add assistant response to chat history.
    st.session_state.messages.append({'role': 'assistant', 'content': response})