# ==================== FILE: routers/inventory.py ====================
from fastapi import APIRouter, HTTPException
from models.ingredient import IngredientCreate
from database import get_db_connection
from psycopg2.extras import RealDictCursor
import psycopg2

router = APIRouter(prefix="/inventory", tags=["Inventory Management"])

@router.post("/ingredients", status_code=201)
def log_ingredient(ingredient: IngredientCreate):
    """Log ingredient delivery"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            data = ingredient.dict()
            if data.get('nutritional_info'):
                data['nutritional_info'] = psycopg2.extras.Json(data['nutritional_info'])
            
            cursor.execute("""
                INSERT INTO ingredients (name, nutritional_info, supplier, 
                                       quantity, unit, expiry_date, 
                                       last_inspection_date, storage_temp)
                VALUES (%(name)s, %(nutritional_info)s, %(supplier)s, 
                        %(quantity)s, %(unit)s, %(expiry_date)s, 
                        %(last_inspection_date)s, %(storage_temp)s)
                RETURNING *
            """, data)
            
            result = dict(cursor.fetchone())
            return {"message": "Ingredient logged", "ingredient": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

