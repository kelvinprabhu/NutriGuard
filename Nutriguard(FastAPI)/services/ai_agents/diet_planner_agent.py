# ==================== FILE: services/ai_agents/diet_planner_agent.py ====================
"""Diet Planning Agent - Creates personalized meal plans"""

from langchain.prompts import PromptTemplate
from .base_agent import BaseAgent
from typing import Dict, Any, Optional, List


class DietPlannerAgent(BaseAgent):
    """
    Specialized agent for creating personalized diet plans
    Considers medical conditions, dietary restrictions, and available recipes
    """
    
    def __init__(self):
        super().__init__(temperature=0.2)
        self.prompt = PromptTemplate(
            input_variables=["patient_info", "recipes_list", "dietitian_notes", "days"],
            template_format="jinja2",
            template="""
You are an expert clinical nutritionist and AI diet planner specializing in healthcare nutrition.

### Your Task:
Create a personalized {%if days > 1 %}{{days}}-day{% else %}daily{% endif %} meal plan for a patient based on their medical profile and dietary needs.

### Patient Profile:
{{ patient_info }}

{% if dietitian_notes %}
### Dietitian's Notes:
{{ dietitian_notes }}
{% endif %}

### Available Recipes (use these preferably):
{{ recipes_list }}

### Instructions:
1. Create a complete meal plan with 5 meals per day: Breakfast, Mid-Morning Snack, Lunch, Evening Snack, Dinner
2. PRIORITIZE using existing recipes from the list above
3. Each meal should be nutritionally balanced and appropriate for the patient's conditions
4. Consider Indian cuisine preferences and traditional dishes
5. Calculate total daily calories and macronutrient distribution
6. If existing recipes don't meet requirements, suggest new recipes to be created
7. Provide specific portion sizes for each meal
8. Include nutritional reasoning for each meal choice

### CRITICAL OUTPUT RULES:
- Output ONLY valid JSON
- NO markdown formatting, backticks, or code blocks
- NO explanatory text before or after JSON
- First character must be `{` and last must be `}`

### Required JSON Structure:
{
  "plan_summary": "Brief 2-3 sentence overview of the diet plan strategy",
  "daily_nutritional_targets": {
    "total_calories": 2000,
    "protein_grams": 120,
    "carbs_grams": 180,
    "fat_grams": 65,
    "fiber_grams": 30,
    "sodium_mg": 1500
  },
  {% if days > 1 %}
  "meal_plans": [
    {
      "day": 1,
      "meals": {
        "breakfast": {
          "recipe_id": 1,
          "recipe_name": "Recipe Name",
          "portion_size": "1 cup",
          "calories": 350,
          "reason": "Why this meal is suitable"
        },
        "mid_morning_snack": {...},
        "lunch": {...},
        "evening_snack": {...},
        "dinner": {...}
      },
      "daily_totals": {
        "calories": 2000,
        "protein": 120,
        "carbs": 180,
        "fats": 65
      }
    }
  ],
  {% else %}
  "meals": {
    "breakfast": {
      "recipe_id": 1,
      "recipe_name": "Recipe Name",
      "portion_size": "1 cup",
      "calories": 350,
      "reason": "Why this meal is suitable"
    },
    "mid_morning_snack": {...},
    "lunch": {...},
    "evening_snack": {...},
    "dinner": {...}
  },
  {% endif %}
  "used_recipe_ids": [1, 2, 3],
  "special_considerations": [
    "Monitor blood sugar levels after meals",
    "Ensure adequate hydration"
  ],
  "add_new_recipes": false,
  "suggested_new_recipes": []
}

If new recipes are needed, set "add_new_recipes": true and include:
"suggested_new_recipes": [
  {
    "name": "Recipe Name",
    "description": "Detailed description",
    "meal_type": "Breakfast/Lunch/Dinner/Snack",
    "reason": "Why this recipe is needed for this patient",
    "key_ingredients": ["ingredient1", "ingredient2"],
    "estimated_calories": 350
  }
]
"""
        )
    
    def generate_meal_plan(self,
                          patient_data: Dict[str, Any],
                          recipes_list: List[Dict[str, Any]],
                          dietitian_notes: Optional[str] = None,
                          days: int = 1) -> Dict[str, Any]:
        """
        Generate personalized meal plan
        
        Args:
            patient_data: Patient medical and dietary information
            recipes_list: Available recipes to choose from
            dietitian_notes: Optional notes from dietitian
            days: Number of days for meal plan (default: 1)
        
        Returns:
            Complete meal plan with nutritional details
        """
        # Format patient info
        patient_info = f"""
Name: {patient_data.get('name', 'Unknown')}
Age: {patient_data.get('age', 'N/A')}
Gender: {patient_data.get('gender', 'N/A')}
Medical Conditions: {patient_data.get('medical_conditions', 'None specified')}
Dietary Restrictions: {patient_data.get('dietary_restrictions', 'None specified')}
"""
        
        # Format recipes list
        recipes_formatted = "\n".join([
            f"ID: {r.get('id')}, Name: {r.get('name')}, "
            f"Calories: {r.get('total_calories', 'N/A')}, "
            f"Description: {r.get('description', 'N/A')}"
            for r in recipes_list
        ])
        
        result = self.invoke_with_search(
            self.prompt,
            {
                "patient_info": patient_info,
                "recipes_list": recipes_formatted if recipes_formatted else "No recipes available",
                "dietitian_notes": dietitian_notes,
                "days": days
            }
        )
        
        return result

