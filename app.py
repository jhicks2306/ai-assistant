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
from sql_chain import get_query_chain
from project_config import ProjectConfig

# Connect to pantry database
DB_PATH = ProjectConfig.DB_PATH
conn, cursor = po.connect_to_db(DB_PATH)

# Set up message history and config (required when calling Chain with history.)
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("PantryPal: How can I help you?")
config = {"configurable": {"session_id": "any"}}

# Set up chain to route user messages to the correct response.
router = get_routing_chain()

# Placeholder function for querying with pantry.
def query_pantry(ingredients):
    return f'This is a pantry query?'

# Set up main chat model chain and pass message history.
model = Ollama(model='mistral:instruct')

prompt = ChatPromptTemplate.from_messages( 
    [
        ("system", "You are a helpful assistant called PantryPal. You are knowledgable about food ingedients, recipes and cooking. Respond to user queries with reference to the pantry that shows which food ingredients are in stock. Provide a natural language response. Be concise and do not make up any food ingredients that are not in the pantry. Start each response with PantryPal: "),
        MessagesPlaceholder(variable_name="history"),
        ("user", """
        Pantry: {pantry}
        Query : {input}
        """)
    ]
)

pantry = po.get_pantry_csv(conn, cursor)
# Chain for when the response comes from the chat LLM.


chain = prompt | model
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="input",
    history_messages_key="history"
)

# Define utility function for streamed responses.
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
        # Call chat model.
        response = chain_with_history.stream({"input": input, "pantry": pantry}, config)

    # Write AI assistant response and add to message history.
    st.chat_message("assistant").write_stream(response)

    cursor.close()
    conn.close()
