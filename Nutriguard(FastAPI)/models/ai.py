# ==================== FILE: models/ai.py ====================
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class MealRecommendationRequest(BaseModel):
    patient_id: int
    preferences: Optional[Dict[str, Any]] = None

class RecipeModifyRequest(BaseModel):
    recipe_id: int
    dietary_requirements: List[str]

class RiskAssessmentRequest(BaseModel):
    ingredient_ids: Optional[List[int]] = None
    facility_areas: Optional[List[str]] = None

class OutcomePredictionRequest(BaseModel):
    patient_id: int
    meal_plan_id: Optional[int] = None
    time_horizon_days: int = 30

class RecipeOptimizeRequest(BaseModel):
    recipe_id: int
    health_goals: List[str]

