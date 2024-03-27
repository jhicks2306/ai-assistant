from pathlib import Path
from rich import print

from langchain.memory import ConversationBufferMemory
from langchain.utilities import SQLDatabase
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

llm = ChatOllama(model='llama2')

# Setup database connection.
db_path = Path.cwd() / 'pantry.db'
rel = db_path.relative_to(Path.cwd())
db_string = f"sqlite:///{rel}"
db = SQLDatabase.from_uri(db_string)

def get_schema(_):
    return db.get_table_info()

def run_query(query):
    return db.run(query)

# Create chain for creating suitable SQL query based on user question.
template = """Based on the table schema below, write a SQL query that would answer the user's question:
{sql_schema}

Question: {question}
SQL Query: """

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Given an input question, convert it to a SQL query. No pre-amble."),
        MessagesPlaceholder(variable_name="history"),
        ("human", template),
    ]
)

memory = ConversationBufferMemory(return_messages=True)

sql_chain = (
    RunnablePassthrough.assign(
        sql_schema=get_schema,
        history=RunnableLambda(lambda x: memory.load_memory_variables(x)["history"]),
    )
    | prompt
    | llm
    | StrOutputParser() # -> should output a string SQL query.
)

def save(input_output):
    output = {"output": input_output.pop("output")}
    memory.save_context(input_output, output)
    return output["output"]

sql_response_memory = RunnablePassthrough.assign(output=sql_chain) | save

# Chain to answer
template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}"""

prompt_response = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given an input question and SQL response, convert it to a natural "
            "language answer. No pre-amble.",
        ),
        ("human", template),
    ]
)

chain = (
    RunnablePassthrough.assign(query=sql_response_memory)
    | RunnablePassthrough.assign(
        schema=get_schema,
        response=lambda x: db.run(x["query"]),
    )
    | prompt_response
    | llm
    | StrOutputParser()
)

print(chain.invoke({'question':"What food items are not in stock?"}))