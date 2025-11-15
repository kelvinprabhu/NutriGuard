# ==================== FILE: services/recipe_service.py ====================
from database import get_db_connection
from psycopg2.extras import RealDictCursor

class RecipeService:
    
    @staticmethod
    def search_recipes(keyword=None, max_calories=None):
        """Search recipes with filters"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = "SELECT * FROM recipes WHERE 1=1"
            params = []
            
            if keyword:
                query += " AND (name ILIKE %s OR description ILIKE %s)"
                params.extend([f"%{keyword}%", f"%{keyword}%"])
            
            if max_calories:
                query += " AND total_calories <= %s"
                params.append(max_calories)
            
            query += " ORDER BY name"
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_recipe(recipe_id: int):
        """Get recipe by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM recipes WHERE id = %s", (recipe_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def create_recipe(recipe_data: dict):
        """Create a new recipe"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                INSERT INTO recipes (name, description, image_url, 
                                   total_calories, created_by)
                VALUES (%(name)s, %(description)s, %(image_url)s,
                        %(total_calories)s, %(created_by)s)
                RETURNING *
            """, recipe_data)
            return dict(cursor.fetchone())
