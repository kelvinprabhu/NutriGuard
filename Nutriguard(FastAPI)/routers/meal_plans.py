from fastapi import APIRouter, HTTPException
from services.meal_plan_service import MealPlanService
from services.patient_service import PatientService
from services.ai_service import AIService
from datetime import date, timedelta

router = APIRouter(prefix="/meal-plans", tags=["Meal Planning"])

@router.post("/generate")
def generate_meal_plan(patient_id: int, days: int = 7):
    """
    AI generates meal plan for patient
    
    Args:
        patient_id: ID of the patient
        days: Number of days for the meal plan (default: 7)
    
    Returns:
        Generated meal plan with AI recommendations
    """
    try:
        # Get patient details
        patient = PatientService.get_patient(patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        # Get AI recommendations based on patient data
        ai_recommendations = AIService.generate_meal_recommendations(patient)
        
        # Create meal plan in database
        start_date = date.today()
        end_date = start_date + timedelta(days=days)
        
        meal_plan_data = {
            "patient_id": patient_id,
            "start_date": start_date,
            "end_date": end_date,
            "ai_generated": True,
            "notes": "AI-generated meal plan based on medical conditions and dietary restrictions",
            "created_by": None
        }
        
        meal_plan = MealPlanService.create_meal_plan(meal_plan_data)
        
        return {
            "message": "Meal plan generated successfully",
            "meal_plan": meal_plan,
            "ai_recommendations": ai_recommendations
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{meal_plan_id}/images")
def generate_meal_cards(meal_plan_id: int):
    """
    Generate visual meal cards for a meal plan
    
    Args:
        meal_plan_id: ID of the meal plan
    
    Returns:
        Generated meal cards with images
    """
    try:
        from database import get_db_connection
        from psycopg2.extras import RealDictCursor
        
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get all recipes in the meal plan
            cursor.execute("""
                SELECT mpr.*, r.name, r.description, r.image_url
                FROM meal_plan_recipes mpr
                JOIN recipes r ON mpr.recipe_id = r.id
                WHERE mpr.meal_plan_id = %s
            """, (meal_plan_id,))
            
            recipes = cursor.fetchall()
            
            if not recipes:
                raise HTTPException(
                    status_code=404, 
                    detail="Meal plan not found or contains no recipes"
                )
            
            # Generate meal cards (dummy implementation)
            meal_cards = []
            for recipe in recipes:
                meal_cards.append({
                    "recipe_id": recipe['recipe_id'],
                    "recipe_name": recipe['name'],
                    "meal_type": recipe['meal_type'],
                    "portion_size": recipe['portion_size'],
                    "description": recipe['description'],
                    "image_url": recipe['image_url'] or f"https://placeholder.com/meal-{recipe['recipe_id']}.jpg",
                    "card_generated": True
                })
            
            return {
                "meal_plan_id": meal_plan_id,
                "cards_generated": len(meal_cards),
                "meal_cards": meal_cards
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{meal_plan_id}")
def get_meal_plan(meal_plan_id: int):
    """
    Get meal plan details by ID
    
    Args:
        meal_plan_id: ID of the meal plan
    
    Returns:
        Meal plan with all recipes
    """
    try:
        from database import get_db_connection
        from psycopg2.extras import RealDictCursor
        
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Get meal plan
            cursor.execute("""
                SELECT mp.*, s.name as created_by_name,
                       p.name as patient_name
                FROM meal_plans mp
                LEFT JOIN staff s ON mp.created_by = s.id
                LEFT JOIN patients p ON mp.patient_id = p.id
                WHERE mp.id = %s
            """, (meal_plan_id,))
            
            meal_plan = cursor.fetchone()
            
            if not meal_plan:
                raise HTTPException(status_code=404, detail="Meal plan not found")
            
            # Get recipes
            cursor.execute("""
                SELECT mpr.*, r.name as recipe_name, r.description, 
                       r.total_calories, r.image_url
                FROM meal_plan_recipes mpr
                JOIN recipes r ON mpr.recipe_id = r.id
                WHERE mpr.meal_plan_id = %s
                ORDER BY 
                    CASE mpr.meal_type
                        WHEN 'Breakfast' THEN 1
                        WHEN 'Lunch' THEN 2
                        WHEN 'Dinner' THEN 3
                        WHEN 'Snack' THEN 4
                    END
            """, (meal_plan_id,))
            
            recipes = cursor.fetchall()
            
            result = dict(meal_plan)
            result['recipes'] = [dict(r) for r in recipes]
            
            return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{meal_plan_id}/recipes")
def add_recipe_to_meal_plan(
    meal_plan_id: int,
    recipe_id: int,
    meal_type: str,
    portion_size: str = None
):
    """
    Add a recipe to a meal plan
    
    Args:
        meal_plan_id: ID of the meal plan
        recipe_id: ID of the recipe to add
        meal_type: Type of meal (Breakfast, Lunch, Dinner, Snack)
        portion_size: Portion size description
    
    Returns:
        Success message with added recipe details
    """
    try:
        from database import get_db_connection
        from psycopg2.extras import RealDictCursor
        from utils.enums import MealType
        
        # Validate meal type
        valid_meal_types = [mt.value for mt in MealType]
        if meal_type not in valid_meal_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid meal type. Must be one of: {', '.join(valid_meal_types)}"
            )
        
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Check if meal plan exists
            cursor.execute("SELECT id FROM meal_plans WHERE id = %s", (meal_plan_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Meal plan not found")
            
            # Check if recipe exists
            cursor.execute("SELECT id FROM recipes WHERE id = %s", (recipe_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Recipe not found")
            
            # Add recipe to meal plan
            cursor.execute("""
                INSERT INTO meal_plan_recipes (meal_plan_id, recipe_id, meal_type, portion_size)
                VALUES (%s, %s, %s, %s)
                RETURNING *
            """, (meal_plan_id, recipe_id, meal_type, portion_size))
            
            result = dict(cursor.fetchone())
            
            return {
                "message": "Recipe added to meal plan successfully",
                "meal_plan_recipe": result
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{meal_plan_id}/recipes/{recipe_id}")
def remove_recipe_from_meal_plan(meal_plan_id: int, recipe_id: int):
    """
    Remove a recipe from a meal plan
    
    Args:
        meal_plan_id: ID of the meal plan
        recipe_id: ID of the recipe to remove
    
    Returns:
        Success message
    """
    try:
        from database import get_db_connection
        from psycopg2.extras import RealDictCursor
        
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                DELETE FROM meal_plan_recipes
                WHERE meal_plan_id = %s AND recipe_id = %s
                RETURNING id
            """, (meal_plan_id, recipe_id))
            
            deleted = cursor.fetchone()
            
            if not deleted:
                raise HTTPException(
                    status_code=404,
                    detail="Recipe not found in this meal plan"
                )
            
            return {
                "message": "Recipe removed from meal plan successfully"
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patient/{patient_id}/active")
def get_patient_active_meal_plans(patient_id: int):
    """
    Get all active meal plans for a patient
    
    Args:
        patient_id: ID of the patient
    
    Returns:
        List of active meal plans
    """
    try:
        from database import get_db_connection
        from psycopg2.extras import RealDictCursor
        
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT mp.*, s.name as created_by_name,
                       COUNT(mpr.id) as recipe_count
                FROM meal_plans mp
                LEFT JOIN staff s ON mp.created_by = s.id
                LEFT JOIN meal_plan_recipes mpr ON mp.id = mpr.meal_plan_id
                WHERE mp.patient_id = %s 
                AND mp.start_date <= CURRENT_DATE 
                AND mp.end_date >= CURRENT_DATE
                GROUP BY mp.id, s.name
                ORDER BY mp.created_at DESC
            """, (patient_id,))
            
            meal_plans = [dict(row) for row in cursor.fetchall()]
            
            return {
                "patient_id": patient_id,
                "active_meal_plans_count": len(meal_plans),
                "meal_plans": meal_plans
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patient/{patient_id}/history")
def get_patient_meal_plan_history(patient_id: int, limit: int = 10):
    """
    Get meal plan history for a patient
    
    Args:
        patient_id: ID of the patient
        limit: Maximum number of meal plans to return
    
    Returns:
        List of past meal plans
    """
    try:
        from database import get_db_connection
        from psycopg2.extras import RealDictCursor
        
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT mp.*, s.name as created_by_name,
                       COUNT(mpr.id) as recipe_count
                FROM meal_plans mp
                LEFT JOIN staff s ON mp.created_by = s.id
                LEFT JOIN meal_plan_recipes mpr ON mp.id = mpr.meal_plan_id
                WHERE mp.patient_id = %s
                GROUP BY mp.id, s.name
                ORDER BY mp.created_at DESC
                LIMIT %s
            """, (patient_id, limit))
            
            meal_plans = [dict(row) for row in cursor.fetchall()]
            
            return {
                "patient_id": patient_id,
                "total_meal_plans": len(meal_plans),
                "meal_plans": meal_plans
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{meal_plan_id}")
def update_meal_plan(
    meal_plan_id: int,
    start_date: date = None,
    end_date: date = None,
    notes: str = None
):
    """
    Update meal plan details
    
    Args:
        meal_plan_id: ID of the meal plan
        start_date: New start date
        end_date: New end date
        notes: Updated notes
    
    Returns:
        Updated meal plan
    """
    try:
        from database import get_db_connection
        from psycopg2.extras import RealDictCursor
        
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Build update query dynamically
            updates = []
            params = []
            
            if start_date:
                updates.append("start_date = %s")
                params.append(start_date)
            
            if end_date:
                updates.append("end_date = %s")
                params.append(end_date)
            
            if notes is not None:
                updates.append("notes = %s")
                params.append(notes)
            
            if not updates:
                raise HTTPException(
                    status_code=400,
                    detail="No fields to update"
                )
            
            updates.append("updated_at = NOW()")
            params.append(meal_plan_id)
            
            query = f"""
                UPDATE meal_plans 
                SET {', '.join(updates)}
                WHERE id = %s
                RETURNING *
            """
            
            cursor.execute(query, params)
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail="Meal plan not found")
            
            return {
                "message": "Meal plan updated successfully",
                "meal_plan": dict(result)
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{meal_plan_id}")
def delete_meal_plan(meal_plan_id: int):
    """
    Delete a meal plan
    
    Args:
        meal_plan_id: ID of the meal plan to delete
    
    Returns:
        Success message
    """
    try:
        from database import get_db_connection
        from psycopg2.extras import RealDictCursor
        
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                DELETE FROM meal_plans
                WHERE id = %s
                RETURNING id
            """, (meal_plan_id,))
            
            deleted = cursor.fetchone()
            
            if not deleted:
                raise HTTPException(status_code=404, detail="Meal plan not found")
            
            return {
                "message": "Meal plan deleted successfully",
                "meal_plan_id": deleted['id']
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))