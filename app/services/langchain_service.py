from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from typing import List
from ..models.schemas import RecipeCreate
from ..utils.config import get_settings
import os
from fastapi import HTTPException

settings = get_settings()
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

RECIPE_PROMPT = """Extract structured recipe information from the following text.
Pay special attention to quantities, units, and ingredient lists.

Text: {text}

Requirements:
1. Extract recipe name
2. Identify cuisine type if mentioned
3. Get preparation and cooking times
4. List all ingredients with their quantities and units
5. Extract detailed instructions
6. Determine difficulty level
7. Identify taste profile (sweet, savory, spicy, etc.)

{format_instructions}

If any field is not explicitly mentioned in the text, use reasonable defaults based on the recipe context.
Make sure all ingredients mentioned in instructions are included in the ingredients list.
"""

class LangChainService:
    def __init__(self):
        # For general recipe understanding - higher temperature for more creative interpretation
        self.recipe_llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")
        # For precise parsing - zero temperature for consistency
        self.parser_llm = ChatOpenAI(temperature=0)

    def parse_recipe(self, text: str) -> RecipeCreate:
        """Parse unstructured recipe text into structured format"""
        try:
            parser = PydanticOutputParser(pydantic_object=RecipeCreate)
            prompt = PromptTemplate(
                template=RECIPE_PROMPT,
                input_variables=["text"],
                partial_variables={"format_instructions": parser.get_format_instructions()}
            )
            
            # First pass - extract structured data
            chain = prompt | self.parser_llm | parser
            recipe = chain.invoke({"text": text})
            
            # Second pass - enrich with additional context
            enrichment_prompt = f"""Review this recipe and add any missing information:
            {recipe.dict()}
            
            Add:
            1. Reasonable time estimates if missing
            2. Difficulty level based on steps
            3. Taste profile based on ingredients
            4. Cuisine type based on ingredients and style
            """
            
            enrichment = self.recipe_llm.predict(enrichment_prompt)
            return recipe
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse recipe: {str(e)}")

    def get_recipe_suggestions(self, query: str, available_ingredients: List[str]) -> str:
        """Get recipe suggestions based on query and available ingredients"""
        try:
            prompt = f"""
            Based on these available ingredients: {', '.join(available_ingredients)}
            And the user's request: {query}
            
            Suggest suitable recipes following these rules:
            1. Prioritize recipes where most ingredients are available
            2. For each suggested recipe:
               - List which available ingredients can be used
               - Specify what additional ingredients are needed
               - Explain why this recipe matches the user's request
            3. If the user has dietary preferences in their request, respect them
            4. Include preparation time and difficulty level
            
            Format suggestions clearly with bullet points and sections.
            """
            
            response = self.recipe_llm.predict(prompt)
            return response
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to get suggestions: {str(e)}")

# Create a singleton instance
langchain_service = LangChainService()