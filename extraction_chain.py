from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains import create_extraction_chain, create_extraction_chain_pydantic
from typing import Optional
from langchain_core.prompts import PromptTemplate

llm = OllamaFunctions(model="llama2")

class Ingredient(BaseModel):
    """Information about a food ingredient."""
    name: Optional[str] = Field(None, description="The name of the food ingredient.")
    # in_stock: Optional[bool] = Field(None, description="True if in stock. False if not in stock.")

template = """Extract all food ingredients from the following passage and record whether they are in or out of stock."""
prompt = PromptTemplate.from_template(template)
# Schema
# schema = {
#     "properties": {
#         "food_ingredient": {"type": "string"},
#         "in_stock": {"type": "boolean"},
#     },
#     "required": ["food_ingredient", "in_stock"],
# }

# chain = create_extraction_chain(schema, llm)
chain = create_extraction_chain_pydantic(pydantic_schema=Ingredient, llm=llm, verbose=True)
input = "I went to the supermarket and bought apples, oranges and bananas. Pasta and yoghurt are to be recorded as not in stock."
input2 = "I used up the apples and bananas"
print(chain.invoke(input2))