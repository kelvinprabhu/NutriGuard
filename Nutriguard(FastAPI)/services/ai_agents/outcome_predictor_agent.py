# ==================== FILE: services/ai_agents/outcome_predictor_agent.py ====================
"""Outcome Prediction Agent - Wrapper for nutrition analyst predictions"""

from .nutrition_analyst_agent import NutritionAnalystAgent
from typing import Dict, Any, List


class OutcomePredictorAgent:
    """
    Specialized agent for predicting health outcomes
    This is a wrapper around NutritionAnalystAgent's prediction capabilities
    """
    
    def __init__(self):
        self.analyst = NutritionAnalystAgent()
    
    def predict_outcomes(self,
                        patient_data: Dict[str, Any],
                        meal_plan: Dict[str, Any],
                        historical_data: List[Dict[str, Any]],
                        time_horizon_days: int = 30) -> Dict[str, Any]:
        """
        Predict health outcomes
        
        Delegates to NutritionAnalystAgent
        """
        return self.analyst.predict_outcomes(
            patient_data,
            meal_plan,
            historical_data,
            time_horizon_days
        )


# ==================== FILE: services/ai_

