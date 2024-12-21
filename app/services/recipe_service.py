from typing import List, Optional
import uuid
from fastapi import HTTPException
from datetime import datetime
from ..models.schemas import RecipeCreate, Recipe, IngredientCreate, Ingredient
from .langchain_service import langchain_service
from supabase import create_client
from ..utils.config import get_settings

settings = get_settings()
supabase = create_client(settings.supabase_url, settings.supabase_key)

class RecipeService:
    @staticmethod
    async def create_recipe(recipe: RecipeCreate, user_id: str) -> Recipe:
        """Create a new recipe"""
        try:
            # Generate vector store ID
            vector_store_id = str(uuid.uuid4())
            
            # Prepare recipe data
            recipe_data = {
                **recipe.dict(exclude={'ingredients'}),
                "user_id": user_id,
                "vector_store_id": vector_store_id,
                "average_rating": 0.0,
                "number_of_reviews": 0,
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Add to Supabase
            recipe_response = supabase.table("recipes").insert(recipe_data).execute()
            
            if not recipe_response.data:
                raise HTTPException(status_code=400, detail="Failed to create recipe")
            
            recipe_id = recipe_response.data[0]["id"]
            
            # Add recipe ingredients
            ingredient_data = [
                {
                    "recipe_id": recipe_id,
                    **ingredient.dict(),
                }
                for ingredient in recipe.ingredients
            ]
            
            ingredients_response = supabase.table("recipe_ingredients").insert(ingredient_data).execute()
            
            if not ingredients_response.data:
                # Cleanup if ingredients insertion fails
                supabase.table("recipes").delete().eq("id", recipe_id).execute()
                raise HTTPException(status_code=400, detail="Failed to add recipe ingredients")
            
            return Recipe(**recipe_response.data[0])
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_recipes(user_id: str) -> List[Recipe]:
        """Get all recipes with their ingredients for a user"""
        try:
            # Get recipes
            recipe_response = supabase.table("recipes")\
                .select("*, recipe_ingredients(*)")\
                .eq("user_id", user_id)\
                .execute()
            
            if not recipe_response.data:
                return []
                
            # Convert to Recipe objects
            recipes = []
            for recipe_data in recipe_response.data:
                ingredients = recipe_data.pop("recipe_ingredients", [])
                recipe = Recipe(
                    **recipe_data,
                    ingredients=ingredients
                )
                recipes.append(recipe)
                
            return recipes
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_recipe(recipe_id: int, user_id: str) -> Optional[Recipe]:
        """Get a specific recipe with ingredients"""
        try:
            response = supabase.table("recipes")\
                .select("*, recipe_ingredients(*)")\
                .eq("id", recipe_id)\
                .eq("user_id", user_id)\
                .single()\
                .execute()
                
            if not response.data:
                return None
                
            recipe_data = response.data
            ingredients = recipe_data.pop("recipe_ingredients", [])
            return Recipe(
                **recipe_data,
                ingredients=ingredients
            )
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def update_recipe(recipe_id: int, recipe: RecipeCreate, user_id: str) -> Recipe:
        """Update a recipe and its ingredients"""
        try:
            # Verify ownership
            existing_recipe = await RecipeService.get_recipe(recipe_id, user_id)
            if not existing_recipe:
                raise HTTPException(status_code=404, detail="Recipe not found")
            
            # Update recipe
            recipe_data = recipe.dict(exclude={'ingredients'})
            recipe_response = supabase.table("recipes")\
                .update(recipe_data)\
                .eq("id", recipe_id)\
                .execute()
                
            # Update ingredients
            # First delete existing
            supabase.table("recipe_ingredients")\
                .delete()\
                .eq("recipe_id", recipe_id)\
                .execute()
                
            # Then add new
            ingredient_data = [
                {
                    "recipe_id": recipe_id,
                    **ingredient.dict(),
                }
                for ingredient in recipe.ingredients
            ]
            
            supabase.table("recipe_ingredients")\
                .insert(ingredient_data)\
                .execute()
                
            return Recipe(**recipe_response.data[0])
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def delete_recipe(recipe_id: int, user_id: str):
        """Delete a recipe"""
        try:
            # Verify ownership
            recipe = await RecipeService.get_recipe(recipe_id, user_id)
            if not recipe:
                raise HTTPException(status_code=404, detail="Recipe not found")
            
            # Delete from Supabase
            # (recipe_ingredients will be deleted automatically due to CASCADE)
            response = supabase.table("recipes")\
                .delete()\
                .eq("id", recipe_id)\
                .execute()
                
            return {"message": "Recipe deleted successfully"}
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def add_ingredient(ingredient: IngredientCreate, user_id: str) -> Ingredient:
        """Add a new ingredient"""
        try:
            ingredient_data = {
                **ingredient.dict(),
                "user_id": user_id,
                "last_updated": datetime.utcnow().isoformat()
            }
            
            response = supabase.table("ingredients").insert(ingredient_data).execute()
            
            if not response.data:
                raise HTTPException(status_code=400, detail="Failed to add ingredient")
                
            return Ingredient(**response.data[0])
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_ingredients(user_id: str) -> List[Ingredient]:
        """Get all ingredients for a user"""
        try:
            response = supabase.table("ingredients")\
                .select("*")\
                .eq("user_id", user_id)\
                .execute()
                
            return [Ingredient(**ing) for ing in response.data] if response.data else []
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def update_ingredient(
        ingredient_id: int,
        ingredient: IngredientCreate,
        user_id: str
    ) -> Ingredient:
        """Update an ingredient"""
        try:
            # Verify ownership
            existing = supabase.table("ingredients")\
                .select("*")\
                .eq("id", ingredient_id)\
                .eq("user_id", user_id)\
                .single()\
                .execute()
                
            if not existing.data:
                raise HTTPException(
                    status_code=404,
                    detail="Ingredient not found or access denied"
                )
                
            update_data = {
                **ingredient.dict(),
                "last_updated": datetime.utcnow().isoformat()
            }
            
            response = supabase.table("ingredients")\
                .update(update_data)\
                .eq("id", ingredient_id)\
                .execute()
                
            return Ingredient(**response.data[0])
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def delete_ingredient(ingredient_id: int, user_id: str):
        """Delete an ingredient"""
        try:
            # Verify ownership
            existing = supabase.table("ingredients")\
                .select("*")\
                .eq("id", ingredient_id)\
                .eq("user_id", user_id)\
                .single()\
                .execute()
                
            if not existing.data:
                raise HTTPException(
                    status_code=404,
                    detail="Ingredient not found or access denied"
                )
                
            supabase.table("ingredients")\
                .delete()\
                .eq("id", ingredient_id)\
                .execute()
                
            return {"message": "Ingredient deleted successfully"}
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def get_recipe_suggestions(query: str, user_id: str) -> str:
        """Get recipe suggestions based on available ingredients"""
        try:
            # Get available ingredients
            ingredients = await RecipeService.get_ingredients(user_id)
            available_ingredients = [ing.name for ing in ingredients]
            
            # Get suggestions from LangChain
            return langchain_service.get_recipe_suggestions(query, available_ingredients)
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

# Create singleton instance
recipe_service = RecipeService()