# ==================== FILE: models/meal_plan.py ====================
from pydantic import BaseModel
from typing import Optional
from datetime import date
from utils.enums import MealType

class MealPlanCreate(BaseModel):
    patient_id: int
    created_by: Optional[int] = None
    start_date: date
    end_date: date
    ai_generated: bool = False
    notes: Optional[str] = None

class MealPlanRecipe(BaseModel):
    recipe_id: int
    meal_type: MealType
    portion_size: Optional[str] = None

