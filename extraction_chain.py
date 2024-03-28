from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains import create_extraction_chain, create_extraction_chain_pydantic
from typing import Optional
from langchain_core.prompts import PromptTemplate

def get_extraction_chain():
    llm = OllamaFunctions(model="llama2")

    class Ingredient(BaseModel):
        """Information about a food ingredient."""

        name: Optional[str] = Field(None, description="The name of the food ingredient.")
        # quantity: Optional[int] = Field(None, description="Amount of the food ingredient.")
        # unit: Optional[str] = Field(None, description="Unit of measurement.")
        # in_stock: Optional[bool] = Field(None, description="True if in stock. False if not in stock.")

    chain = create_extraction_chain_pydantic(pydantic_schema=Ingredient, llm=llm, verbose=True)

    return chain

if __name__ == "__main__":

    chain = get_extraction_chain()
    input = "I went to the supermarket and bought five apples, 3 oranges, some bananas and a pint of milk. I also purchased 400g of pasta."
    print(chain.invoke(input))