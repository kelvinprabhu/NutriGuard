# ==================== FILE: models/__init__.py ====================
# Create this file to make models a package
# Leave it empty or add imports for convenience

from models.patient import PatientCreate, PatientUpdate, DietaryRestrictionUpdate, PatientResponse
from models.recipe import RecipeCreate, RecipeIngredient
from models.meal_plan import MealPlanCreate, MealPlanRecipe
from models.ingredient import IngredientCreate
from models.safety import TemperatureLog, SafetyInspection
from models.nutrition import NutritionIntake
from models.ai import (
    MealRecommendationRequest,
    RecipeModifyRequest,
    RiskAssessmentRequest,
    OutcomePredictionRequest,
    RecipeOptimizeRequest
)

__all__ = [
    # Patient models
    "PatientCreate",
    "PatientUpdate",
    "DietaryRestrictionUpdate",
    "PatientResponse",
    # Recipe models
    "RecipeCreate",
    "RecipeIngredient",
    # Meal plan models
    "MealPlanCreate",
    "MealPlanRecipe",
    # Ingredient models
    "IngredientCreate",
    # Safety models
    "TemperatureLog",
    "SafetyInspection",
    # Nutrition models
    "NutritionIntake",
    # AI models
    "MealRecommendationRequest",
    "RecipeModifyRequest",
    "RiskAssessmentRequest",
    "OutcomePredictionRequest",
    "RecipeOptimizeRequest",
]
# ==================== END OF FILE: models/__init__.py ====================