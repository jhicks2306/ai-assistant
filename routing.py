from langchain_experimental.llms.ollama_functions import OllamaFunctions

def get_routing_chain():

    model = OllamaFunctions(model="mistral:instruct")
    model = model.bind(
        functions=[
        {
            "name": "add_ingredients",
            "description": "Add food ingredients to the pantry (useful when the user buys food)",
            "parameters": {
                "type": "object",
                "properties": {
                    "ingredients": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "A list of food ingredients, e.g. [\"Apples\", \"Bananas\", \"Pasta\"]"
                    },
                },
                "required": ["ingredients"]
            }
        },
        {
            "name": "remove_ingredients",
            "description": "Remove food ingredients from the pantry (useful when the user eats or uses ingredients).",
            "parameters": {
                "type": "object",
                "properties": {
                    "ingredients": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "A list of food ingredients, e.g. [\"Apples\", \"Brazil nuts\", \"Bananas\"]"
                    },
                },
                "required": ["ingredients"]
            }
        },
        {
            "name": "query_pantry",
            "description": "Look up information about what is in the pantry (useful when the user asks questions about what to cook).",
            "parameters": {
                "type": "object",
                "properties": {
                    "ingredients": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "A list of food ingredients, e.g. [\"Apples\", \"Bananas\"]"
                    },
                },
            }
        }
    ]
    )

    return model


if __name__ == "__main__":
    model = OllamaFunctions(model="mistral:instruct")
    print(model.invoke("Do I have hummus and apple?"))

# print(model.invoke("I went to the supermarket and got five apples, 3 oranges, 2 bananas, a pint of milk, and pasta."))

# print(model.invoke("Give me a recipe which uses only items in the pantry."))