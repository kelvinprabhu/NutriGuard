# ==================== FILE: services/ai_agents/__init__.py ====================
"""
Multi-Agent AI System for NutriGuard
Each agent specializes in a specific healthcare nutrition task
"""

from .diet_planner_agent import DietPlannerAgent
from .recipe_modifier_agent import RecipeModifierAgent
from .nutrition_analyst_agent import NutritionAnalystAgent
from .safety_inspector_agent import SafetyInspectorAgent
from .outcome_predictor_agent import OutcomePredictorAgent

__all__ = [
    'DietPlannerAgent',
    'RecipeModifierAgent',
    'NutritionAnalystAgent',
    'SafetyInspectorAgent',
    'OutcomePredictorAgent'
]