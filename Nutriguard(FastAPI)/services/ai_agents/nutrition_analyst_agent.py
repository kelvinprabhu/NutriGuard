# ==================== FILE: services/ai_agents/nutrition_analyst_agent.py ====================
"""Nutrition Analysis Agent - Analyzes patient nutrition data and outcomes"""

from langchain.prompts import PromptTemplate
from .base_agent import BaseAgent
from typing import Dict, Any, List


class NutritionAnalystAgent(BaseAgent):
    """
    Specialized agent for analyzing nutrition data and health correlations
    Provides insights on dietary patterns and health outcomes
    """
    
    def __init__(self):
        super().__init__(temperature=0.1)
        
        self.correlation_prompt = PromptTemplate(
            input_variables=["patient_info", "nutrition_entries", "analysis_period"],
            template_format="jinja2",
            template="""
You are an expert clinical nutrition data analyst specializing in health outcome correlations.

### Patient Information:
{{ patient_info }}

### Nutrition Data (Last {{ analysis_period }} days):
{{ nutrition_entries }}

### Your Task:
Analyze the correlation between dietary intake and health outcomes (blood sugar, symptoms, etc.).
Identify patterns, trends, and provide actionable recommendations.

### CRITICAL OUTPUT RULES:
- Output ONLY valid JSON
- NO markdown or extra text
- First character must be `{` and last must be `}`

### Required JSON Structure:
{
  "analysis_summary": "2-3 sentence overview of key findings",
  "data_quality": {
    "entries_analyzed": 30,
    "data_completeness": "85%",
    "reliability_score": 0.88
  },
  "correlations_found": [
    {
      "factor": "High carbohydrate meals",
      "health_metric": "Blood sugar levels",
      "correlation_strength": "Strong positive",
      "average_impact": "+18 mg/dL spike",
      "evidence": "Observed in 85% of high-carb meals",
      "recommendation": "Reduce simple carbs, increase fiber"
    }
  ],
  "trends": {
    "blood_sugar": {
      "current_average": 128.5,
      "previous_average": 135.2,
      "trend": "Improving",
      "change_percentage": -5.0
    },
    "meal_compliance": {
      "average_intake_percentage": 87.5,
      "trend": "Stable"
    },
    "nutritional_balance": {
      "protein_adequacy": "Good",
      "carb_management": "Needs improvement",
      "micronutrients": "Adequate"
    }
  },
  "best_performing_meals": [
    {
      "meal_name": "Grilled chicken salad",
      "reason": "Stable blood sugar, high satiety",
      "frequency": 8,
      "avg_blood_sugar_2hr": 115
    }
  ],
  "meals_to_modify": [
    {
      "meal_name": "Pasta with tomato sauce",
      "issue": "Blood sugar spikes",
      "suggestion": "Replace with whole grain pasta, add protein"
    }
  ],
  "actionable_recommendations": [
    {
      "priority": "High",
      "recommendation": "Increase fiber intake by 10g/day",
      "expected_benefit": "Better glycemic control",
      "implementation": "Add 1 cup of vegetables to lunch and dinner"
    }
  ],
  "risk_alerts": [],
  "positive_changes": []
}
"""
        )
        
        self.outcome_prediction_prompt = PromptTemplate(
            input_variables=["patient_info", "current_meal_plan", "historical_data", "time_horizon"],
            template_format="jinja2",
            template="""
You are an expert predictive health analytics AI specializing in nutrition outcomes.

### Patient Information:
{{ patient_info }}

### Current Meal Plan:
{{ current_meal_plan }}

### Historical Health Data:
{{ historical_data }}

### Prediction Timeframe:
{{ time_horizon }} days

### Your Task:
Predict health outcomes based on the current meal plan and historical patterns.
Provide confidence intervals and risk assessments.

### CRITICAL OUTPUT RULES:
- Output ONLY valid JSON
- NO markdown or extra text

### Required JSON Structure:
{
  "prediction_summary": "Overview of expected outcomes",
  "confidence_level": 0.87,
  "timeframe_days": 30,
  "predicted_outcomes": {
    "blood_sugar_control": {
      "current_average": 128.5,
      "predicted_average": 118.2,
      "confidence_interval": {
        "lower": 115.0,
        "upper": 121.5
      },
      "trend": "Improving",
      "likelihood": "High (85%)"
    },
    "weight_management": {
      "current_kg": 75.0,
      "predicted_change_kg": -1.5,
      "trend": "Gradual decrease",
      "healthy_pace": true
    },
    "nutritional_status": {
      "protein_intake": "Adequate and improving",
      "micronutrient_status": "Good",
      "hydration": "Optimal"
    },
    "symptom_management": {
      "fatigue_levels": "Expected to decrease by 30%",
      "energy_levels": "Expected to improve",
      "digestive_health": "Stable"
    }
  },
  "risk_factors": {
    "hypoglycemia_risk": {
      "level": "Low",
      "probability": "5%",
      "mitigation": "Current meal timing is appropriate"
    },
    "nutrient_deficiency_risk": {
      "level": "Very Low",
      "at_risk_nutrients": [],
      "monitoring_recommended": []
    }
  },
  "milestone_predictions": {
    "week_1": "Initial adaptation, slight improvement in energy",
    "week_2": "Noticeable blood sugar stabilization",
    "week_4": "Significant improvement in overall metrics"
  },
  "recommendations_for_success": [
    "Continue current meal plan with minor adjustments",
    "Monitor blood sugar twice daily",
    "Ensure consistent meal timing"
  ],
  "adjustment_triggers": [
    "If blood sugar drops below 90 mg/dL consistently, increase complex carbs",
    "If weight loss exceeds 2kg/month, increase caloric intake by 10%"
  ]
}
"""
        )
    
    def analyze_correlation(self,
                           patient_data: Dict[str, Any],
                           nutrition_entries: List[Dict[str, Any]],
                           analysis_period_days: int = 30) -> Dict[str, Any]:
        """
        Analyze correlation between diet and health outcomes
        """
        patient_info = f"""
Name: {patient_data.get('name')}
Age: {patient_data.get('age')}
Medical Conditions: {patient_data.get('medical_conditions')}
Dietary Restrictions: {patient_data.get('dietary_restrictions')}
"""
        
        entries_formatted = "\n".join([
            f"Date: {e.get('date')}, Meal: {e.get('recipe_name', 'N/A')}, "
            f"Intake: {e.get('intake_percentage')}%, "
            f"Blood Sugar: {e.get('blood_sugar')} mg/dL, "
            f"Notes: {e.get('notes', 'None')}"
            for e in nutrition_entries[:50]  # Limit to recent entries
        ])
        
        result = self.invoke_with_search(
            self.correlation_prompt,
            {
                "patient_info": patient_info,
                "nutrition_entries": entries_formatted if entries_formatted else "No data available",
                "analysis_period": analysis_period_days
            }
        )
        
        return result
    
    def predict_outcomes(self,
                        patient_data: Dict[str, Any],
                        meal_plan: Dict[str, Any],
                        historical_data: List[Dict[str, Any]],
                        time_horizon_days: int = 30) -> Dict[str, Any]:
        """
        Predict health outcomes based on meal plan
        """
        patient_info = f"""
Name: {patient_data.get('name')}
Age: {patient_data.get('age')}
Medical Conditions: {patient_data.get('medical_conditions')}
Current Health Status: {historical_data[-1] if historical_data else 'N/A'}
"""
        
        meal_plan_formatted = f"""
Duration: {meal_plan.get('start_date')} to {meal_plan.get('end_date')}
AI Generated: {meal_plan.get('ai_generated')}
Notes: {meal_plan.get('notes')}
"""
        
        historical_formatted = "\n".join([
            f"Date: {h.get('date')}, Blood Sugar: {h.get('blood_sugar')}, "
            f"Intake: {h.get('intake_percentage')}%"
            for h in historical_data[-30:]  # Last 30 entries
        ])
        
        result = self.invoke_with_search(
            self.outcome_prediction_prompt,
            {
                "patient_info": patient_info,
                "current_meal_plan": meal_plan_formatted,
                "historical_data": historical_formatted if historical_formatted else "Limited historical data",
                "time_horizon": time_horizon_days
            }
        )
        
        return result

