# ==================== FILE: models/recipe.py ====================
from pydantic import BaseModel
from typing import Optional

class RecipeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    total_calories: Optional[float] = None
    created_by: Optional[int] = None

class RecipeIngredient(BaseModel):
    ingredient_id: int
    quantity: float
    unit: str

