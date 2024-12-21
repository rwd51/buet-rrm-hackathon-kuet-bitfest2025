from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime

class IngredientBase(BaseModel):
    name: str
    quantity: float
    unit: str
    category: Optional[str] = None
    expiry_date: Optional[datetime] = None

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int
    user_id: UUID4
    last_updated: datetime

    class Config:
        from_attributes = True

class RecipeIngredientBase(BaseModel):
    ingredient_name: str
    quantity: float
    unit: str

class RecipeBase(BaseModel):
    name: str
    cuisine_type: Optional[str] = None
    preparation_time: Optional[int] = None
    cooking_time: Optional[int] = None
    difficulty_level: Optional[str] = None
    taste_profile: Optional[str] = None
    instructions: str
    ingredients: List[RecipeIngredientBase]

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    user_id: UUID4
    average_rating: float
    number_of_reviews: int
    vector_store_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str