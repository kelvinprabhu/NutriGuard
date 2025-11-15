# ==================== FILE: routers/nutrition.py ====================
from fastapi import APIRouter, HTTPException
from models.nutrition import NutritionIntake
from services.nutrition_service import NutritionService
from utils.enums import AlertStatus
from typing import Optional

router = APIRouter(prefix="/nutrition", tags=["Nutrition Monitoring"])

@router.post("/intake", status_code=201)
def log_nutrition_intake(intake: NutritionIntake):
    """Log patient meal consumption"""
    try:
        result = NutritionService.log_intake(intake.dict())
        return {"message": "Intake logged", "entry": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics/{patient_id}")
def get_nutrition_insights(patient_id: int, days: int = 30):
    """Get nutrition insights"""
    try:
        analytics = NutritionService.get_analytics(patient_id, days)
        
        if not analytics:
            return {
                "patient_id": patient_id,
                "message": "No nutrition data available"
            }
        
        return {
            "patient_id": patient_id,
            "analysis_period_days": days,
            "insights": {
                "total_meals_logged": analytics['total_meals_logged'],
                "average_intake_percentage": analytics['average_intake_percentage'],
                "average_blood_sugar": analytics['average_blood_sugar'],
                "total_calories_consumed": analytics['total_calories_consumed'],
                "daily_average_calories": analytics['daily_average_calories']
            },
            "recent_entries": analytics['recent_entries']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-correlation")
def analyze_correlation(patient_id: int):
    """AI analyzes health outcomes"""
    try:
        from database import get_db_connection
        from psycopg2.extras import RealDictCursor
        
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT ne.*, r.name as recipe_name, r.total_calories
                FROM nutrition_entries ne
                LEFT JOIN recipes r ON ne.recipe_id = r.id
                WHERE ne.patient_id = %s 
                AND ne.date >= CURRENT_DATE - INTERVAL '30 days'
                ORDER BY ne.date
            """, (patient_id,))
            
            entries = cursor.fetchall()
        
        # Dummy AI Analysis
        return {
            "patient_id": patient_id,
            "analysis_type": "Blood Sugar vs Meal Correlation",
            "data_points_analyzed": len(entries),
            "findings": [
                {
                    "correlation": "High carbohydrate meals",
                    "impact": "Blood sugar spike of 15-20 mg/dL",
                    "recommendation": "Consider lower glycemic index alternatives"
                },
                {
                    "correlation": "High fiber meals",
                    "impact": "More stable blood sugar levels",
                    "recommendation": "Increase fiber-rich foods"
                }
            ],
            "trends": {
                "average_blood_sugar": 125.5,
                "blood_sugar_trend": "Improving (down 5% from last month)"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

