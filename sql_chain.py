from pathlib import Path
from rich import print

from langchain.memory import ConversationBufferMemory
from langchain_community.utilities import SQLDatabase
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

def get_query_chain():
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
            ("human", template),
        ]
    )

    sql_chain = (
        RunnablePassthrough.assign(
            sql_schema=get_schema,
        )
        | prompt
        | llm
        | StrOutputParser() # -> should output a string SQL query.
    )


    # Chain to convert SQL query to natural language response.
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
                "language answer. Be concise. No pre-amble or quotation marks.",
            ),
            ("human", template),
        ]
    )

    chain = ( #-> "question" input by user.
        RunnablePassthrough.assign(query=sql_chain) # add "query"
        | RunnablePassthrough.assign(
            schema=get_schema, # add "schema"
            response=lambda x: run_query(x["query"]), # add "response"
        )
        | prompt_response # pass "question", "query", "schema", "response" to prompt_response
        | llm
        | StrOutputParser()
    )

    return chain


if __name__ == "__main__":

    chain = get_query_chain()
    print(chain.invoke({'question':"What food items are in stock?"}))