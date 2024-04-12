import streamlit as st
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.tools import tool
from langchain.tools.render import render_text_description
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from utils.load_data import create_vector_db
from utils.lemmatizer import lemmatize_sentence
from router import get_routing_chain
import json
from food_list import FoodList
from sql_chain import get_query_chain
from project_config import ProjectConfig
from datetime import date, timedelta
from dotenv import dotenv_values
from operator import itemgetter
import os
from langchain_core.messages import HumanMessage, AIMessage

env_vars = dotenv_values(".env")
os.environ["LANGCHAIN_API_KEY"] = env_vars['LANGCHAIN_API_KEY']
os.environ["LANGCHAIN_TRACING_V2"] = "true"

st.set_page_config(page_title="Chat", page_icon="💬")

# Connect to pantry database
DB_PATH = ProjectConfig.DB_PATH
pantry = FoodList(DB_PATH, table='pantry')

# Set up message history and config (required when calling Chain with history.)
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("PantryPal: How can I help you?")
config = {"configurable": {"session_id": "any"}}

# Set up chain to route user messages to the correct response.
router = get_routing_chain()

# Set up main chat model chain and pass message history.
model = ChatOllama(model='mistral:instruct')

# Define tools available.
@tool
def add(ingredients: list) -> str:
    """Add list of food ingredients e.g. ['apples', 'pasta'] when the user buys food)."""
    response = pantry.create_items(ingredients)
    return response

@tool
def remove(ingredients: list) -> str:
    """Remove list of food ingredients e.g. ['apples', 'pasta'] when the user eats or uses ingredients."""
    response = pantry.delete_items(ingredients)
    return response

@tool
def converse(input: str) -> str:
    "Provide a natural language response using the user input."
    return model.invoke(input).content

tools = [add, remove, converse]

# Configure the system prompts
rendered_tools = render_text_description(tools)

system_prompt = f"""You are an assistant that has access to the following set of tools. Here are the names and descriptions for each tool:

{rendered_tools}

Given the user input, return the name and input of the tool to use. Return your response as a JSON blob with 'name' and 'arguments' keys. The value associated with the 'arguments' key should be a dictionary of tool parameters.
Do not include the '\' character in the response."""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{input}")]
)

# Define a function which returns the chosen tools as a runnable, based on user input.
def tool_chain(model_output):
    tool_map = {tool.name: tool for tool in tools}
    chosen_tool = tool_map[model_output["name"]]
    return itemgetter("arguments") | chosen_tool

chooser = prompt | model | JsonOutputParser()

# prompt = ChatPromptTemplate.from_messages( 
#     [
#         ("system", "You are a helpful assistant called PantryPal. You are knowledgable about food ingedients, recipes and cooking. Provide a natural language response and be concise. Start each response with PantryPal: "),
#         MessagesPlaceholder(variable_name="history"),
#         ("user", """
#         Answer the following query with reference to the list of ingredients available in the pantry below. 
         
#         Ingredients available in the pantry: {pantry_items}
#         Query : {input}
#         """)
#     ]
# )

# pantry_items = pantry.to_string()

# # Chain for when the response comes from the chat LLM.
# chain = prompt | model
# chain_with_history = RunnableWithMessageHistory(
#     chain,
#     lambda session_id: msgs,
#     input_messages_key="input",
#     history_messages_key="history"
# )



# Define utility function for streaming responses.
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
    msgs.add_user_message(input)

    # Invoke router to direct the user input.
    choice = chooser.invoke(input)
    chosen_tool = tool_chain(choice)
    response_gen = chosen_tool.stream(choice)

    # Write AI assistant response and add to message history.
    message = st.chat_message("assistant").write_stream(response_gen)
    msgs.add_ai_message(message)

    pantry.cursor.close()
    pantry.conn.close()
