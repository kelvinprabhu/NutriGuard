# ==================== FILE: services/meal_plan_service.py ====================
from database import get_db_connection
from psycopg2.extras import RealDictCursor
from datetime import date, timedelta

class MealPlanService:
    
    @staticmethod
    def get_active_meal_plan(patient_id: int):
        """Get active meal plan for patient"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT mp.*, s.name as created_by_name
                FROM meal_plans mp
                LEFT JOIN staff s ON mp.created_by = s.id
                WHERE mp.patient_id = %s 
                AND mp.start_date <= CURRENT_DATE 
                AND mp.end_date >= CURRENT_DATE
                ORDER BY mp.created_at DESC
                LIMIT 1
            """, (patient_id,))
            
            meal_plan = cursor.fetchone()
            
            if not meal_plan:
                return None
            
            # Get recipes
            cursor.execute("""
                SELECT mpr.*, r.name as recipe_name, r.description, 
                       r.total_calories, r.image_url
                FROM meal_plan_recipes mpr
                JOIN recipes r ON mpr.recipe_id = r.id
                WHERE mpr.meal_plan_id = %s
            """, (meal_plan['id'],))
            
            recipes = cursor.fetchall()
            
            result = dict(meal_plan)
            result['recipes'] = [dict(r) for r in recipes]
            return result
    
    @staticmethod
    def create_meal_plan(meal_plan_data: dict):
        """Create a new meal plan"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                INSERT INTO meal_plans (patient_id, start_date, end_date, 
                                       ai_generated, notes, created_by)
                VALUES (%(patient_id)s, %(start_date)s, %(end_date)s, 
                        %(ai_generated)s, %(notes)s, %(created_by)s)
                RETURNING *
            """, meal_plan_data)
            return dict(cursor.fetchone())

