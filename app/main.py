from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Header
from fastapi.middleware.cors import CORSMiddleware
from .models.schemas import RecipeCreate, IngredientCreate, ChatRequest, Recipe, Ingredient
from .services.recipe_service import recipe_service
from .services.langchain_service import langchain_service
from .utils.config import get_settings
from typing import List
from jose import jwt
from PIL import Image
import io
import logging

# Add at the top of main.py
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Mofa's Kitchen Buddy",
    description="""
    A smart kitchen management system that helps you keep track of ingredients
    and suggests recipes based on what you have at home.
    
    Features:
    - Manage your ingredient inventory
    - Store and organize recipes
    - Get recipe suggestions based on available ingredients
    - Extract recipes from images
    - Chat with an AI assistant for recipe recommendations
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Recipe endpoints
@app.post("/recipes/", response_model=Recipe, tags=["Recipes"])
async def create_recipe(recipe: RecipeCreate):
    """Create a new recipe"""
    try:
        return await recipe_service.create_recipe(recipe, "test_user")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/recipes/{recipe_id}", response_model=Recipe, tags=["Recipes"])
async def get_recipe(recipe_id: int):
    """Get a specific recipe by ID"""
    try:
        recipe = await recipe_service.get_recipe(recipe_id, "test_user")
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/recipes/", response_model=List[Recipe], tags=["Recipes"])
async def get_recipes():
    """Get all recipes for the current user"""
    try:
        return await recipe_service.get_recipes("test_user")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/recipes/{recipe_id}", response_model=Recipe, tags=["Recipes"])
async def update_recipe(recipe_id: int, recipe: RecipeCreate):
    """Update a specific recipe"""
    try:
        return await recipe_service.update_recipe(recipe_id, recipe, "test_user")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/recipes/{recipe_id}", tags=["Recipes"])
async def delete_recipe(recipe_id: int):
    """Delete a specific recipe"""
    try:
        return await recipe_service.delete_recipe(recipe_id, "test_user")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/recipes/image", response_model=Recipe, tags=["Recipes"])
async def create_recipe_from_image(file: UploadFile = File(...)):
    """Create a recipe from an image"""
    try:
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Extract text from image using LangChain
        recipe = langchain_service.parse_recipe_from_image(image)
        
        # Save recipe
        return await recipe_service.create_recipe(recipe, "test_user")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Ingredient endpoints
@app.post("/ingredients/", response_model=Ingredient, tags=["Ingredients"])
async def create_ingredient(ingredient: IngredientCreate):
    """Add a new ingredient"""
    try:
        return await recipe_service.add_ingredient(ingredient, "test_user")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/ingredients/", response_model=List[Ingredient], tags=["Ingredients"])
async def get_ingredients():
    """Get all ingredients for the current user"""
    try:
        return await recipe_service.get_ingredients("test_user")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/ingredients/{ingredient_id}", response_model=Ingredient, tags=["Ingredients"])
async def update_ingredient(ingredient_id: int, ingredient: IngredientCreate):
    """Update an ingredient"""
    try:
        return await recipe_service.update_ingredient(ingredient_id, ingredient, "test_user")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/ingredients/{ingredient_id}", tags=["Ingredients"])
async def delete_ingredient(ingredient_id: int):
    """Delete a specific ingredient"""
    try:
        return await recipe_service.delete_ingredient(ingredient_id, "test_user")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chat/", tags=["Chat"])
async def chat(request: ChatRequest):
    """Chat with the recipe assistant"""
    try:
        logger.info(f"Received message: {request.message}")
        
        if not request.message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        try:
            logger.info("Calling recipe_service.get_recipe_suggestions")
            response = await recipe_service.get_recipe_suggestions(request.message, "test_user")
            logger.info(f"Got response from service: {response}")
        except Exception as service_error:
            logger.error(f"Service error: {str(service_error)}")
            raise HTTPException(status_code=500, detail=f"Service error: {str(service_error)}")
            
        if not response:
            return {"response": "I couldn't generate a response. Please try again."}
            
        return {"response": response}
    except Exception as e:
        logger.exception("Error in chat endpoint")  # This will log the full stack trace
        raise HTTPException(status_code=400, detail=str(e))
    
# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Check if the system is running"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)