# ==================== FILE: services/ai_agents/recipe_modifier_agent.py ====================
"""Recipe Modification Agent - Adapts recipes for dietary needs"""

from langchain.prompts import PromptTemplate
from .base_agent import BaseAgent
from typing import Dict, Any, List


class RecipeModifierAgent(BaseAgent):
    """
    Specialized agent for modifying recipes to meet dietary restrictions
    Ensures nutritional adequacy while adapting ingredients
    """
    
    def __init__(self):
        super().__init__(temperature=0.1)
        self.prompt = PromptTemplate(
            input_variables=["recipe", "dietary_requirements", "ingredients_list"],
            template_format="jinja2",
            template="""
You are an expert culinary nutritionist specializing in recipe modification for medical dietary needs.

### Original Recipe:
{{ recipe }}

### Dietary Requirements to Meet:
{{ dietary_requirements }}

### Available Ingredients:
{{ ingredients_list }}

### Your Task:
Modify the recipe to meet ALL dietary requirements while:
1. Maintaining nutritional balance
2. Preserving taste and cultural authenticity (especially for Indian cuisine)
3. Using available ingredients when possible
4. Providing specific ingredient substitutions with quantities
5. Calculating updated nutritional values

### CRITICAL OUTPUT RULES:
- Output ONLY valid JSON
- NO markdown, backticks, or extra text
- First character must be `{` and last must be `}`

### Required JSON Structure:
{
  "can_modify": true,
  "modified_recipe": {
    "name": "Modified Recipe Name",
    "description": "How this recipe has been adapted",
    "total_calories": 350,
    "servings": 2,
    "prep_time_minutes": 30,
    "nutritional_info": {
      "protein_g": 25,
      "carbs_g": 30,
      "fat_g": 10,
      "fiber_g": 8,
      "sodium_mg": 400,
      "sugar_g": 5
    },
    "ingredients": [
      {
        "original": "White rice",
        "replacement": "Quinoa",
        "quantity": "1 cup",
        "reason": "Lower glycemic index for diabetes management"
      }
    ],
    "cooking_instructions": [
      "Step 1: Detailed instruction",
      "Step 2: Detailed instruction"
    ]
  },
  "modifications_made": [
    {
      "category": "Sodium Reduction",
      "change": "Removed salt, added herbs and spices",
      "impact": "Sodium reduced by 60%",
      "nutritional_benefit": "Better for hypertension management"
    }
  ],
  "dietary_compliance": {
    "low_sodium": true,
    "diabetic_friendly": true,
    "heart_healthy": true,
    "gluten_free": false
  },
  "health_score_improvement": {
    "original_score": 6.5,
    "modified_score": 8.7,
    "improvement_percentage": 34
  },
  "allergen_warnings": [],
  "special_notes": "Any special preparation or storage instructions"
}

If recipe cannot be modified to meet requirements, set "can_modify": false and explain why.
"""
        )
    
    def modify_recipe(self,
                     recipe_data: Dict[str, Any],
                     dietary_requirements: List[str],
                     available_ingredients: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Modify recipe to meet dietary requirements
        
        Args:
            recipe_data: Original recipe information
            dietary_requirements: List of dietary restrictions/requirements
            available_ingredients: Optional list of available ingredients
        
        Returns:
            Modified recipe with substitutions and nutritional updates
        """
        # Format recipe
        recipe_formatted = f"""
Name: {recipe_data.get('name')}
Description: {recipe_data.get('description', 'N/A')}
Calories: {recipe_data.get('total_calories', 'N/A')}
Current Ingredients: {recipe_data.get('ingredients', 'Not specified')}
"""
        
        # Format requirements
        requirements_formatted = "\n".join([f"- {req}" for req in dietary_requirements])
        
        # Format ingredients
        if available_ingredients:
            ingredients_formatted = "\n".join([
                f"- {ing.get('name')}: {ing.get('quantity')} {ing.get('unit', '')}"
                for ing in available_ingredients
            ])
        else:
            ingredients_formatted = "Use any appropriate substitutes"
        
        result = self.invoke_with_search(
            self.prompt,
            {
                "recipe": recipe_formatted,
                "dietary_requirements": requirements_formatted,
                "ingredients_list": ingredients_formatted
            }
        )
        
        return result
