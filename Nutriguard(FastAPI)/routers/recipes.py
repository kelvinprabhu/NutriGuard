# ==================== FILE: routers/recipes.py (FIXED) ====================
from fastapi import APIRouter, HTTPException
from models.recipe import RecipeCreate
from models.ai import RecipeModifyRequest  # Fixed import
from services.recipe_service import RecipeService
from services.ai_service import AIService

router = APIRouter(prefix="/recipes", tags=["Recipe Management"])

@router.get("/search")
def search_recipes(keyword: str = None, max_calories: float = None):
    """Search recipes"""
    try:
        recipes = RecipeService.search_recipes(keyword, max_calories)
        return {"count": len(recipes), "recipes": recipes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", status_code=201)
def create_recipe(recipe: RecipeCreate):
    """Create new recipe"""
    try:
        result = RecipeService.create_recipe(recipe.dict())
        return {"message": "Recipe created", "recipe": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{recipe_id}/modify")
def modify_recipe(recipe_id: int, request: RecipeModifyRequest):
    """AI modifies recipe for dietary restrictions"""
    try:
        recipe = RecipeService.get_recipe(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        modifications = AIService.modify_recipe(recipe, request.dietary_requirements)
        return {
            "original_recipe": recipe,
            "dietary_requirements": request.dietary_requirements,
            **modifications
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))