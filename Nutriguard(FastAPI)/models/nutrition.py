# ==================== FILE: models/nutrition.py ====================
from pydantic import BaseModel
from typing import Optional
from datetime import date

class NutritionIntake(BaseModel):
    patient_id: int
    recipe_id: Optional[int] = None
    recorded_by: Optional[int] = None
    date: Optional[date] = None
    intake_percentage: Optional[float] = None
    blood_sugar: Optional[float] = None
    notes: Optional[str] = None

