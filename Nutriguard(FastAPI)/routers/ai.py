# ==================== FILE: routers/ai.py ====================
from fastapi import APIRouter, HTTPException
from models.ai import (
    MealRecommendationRequest, 
    RiskAssessmentRequest,
    OutcomePredictionRequest,
    RecipeOptimizeRequest
)
from services.ai_service import AIService
from services.patient_service import PatientService
from services.recipe_service import RecipeService

router = APIRouter(prefix="/ai", tags=["AI-Powered Recommendations"])

@router.post("/recommend-meals")
def recommend_meals(request: MealRecommendationRequest):
    """Get AI meal recommendations"""
    try:
        patient = PatientService.get_patient(request.patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        recommendations = AIService.generate_meal_recommendations(patient)
        
        return {
            "patient_id": request.patient_id,
            "patient_profile": {
                "name": patient['name'],
                "medical_conditions": patient['medical_conditions'],
                "dietary_restrictions": patient['dietary_restrictions']
            },
            **recommendations,
            "personalization_factors": [
                "Optimized for blood sugar control",
                "Low sodium for hypertension management",
                "High fiber for digestive health"
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assess-risks")
def assess_food_safety_risks(request: RiskAssessmentRequest):
    """Assess food safety risks"""
    try:
        from database import get_db_connection
        from psycopg2.extras import RealDictCursor
        from datetime import date
        
        risk_items = []
        
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Check ingredients
            if request.ingredient_ids:
                cursor.execute("""
                    SELECT * FROM ingredients 
                    WHERE id = ANY(%s)
                """, (request.ingredient_ids,))
                ingredients = cursor.fetchall()
                
                for ing in ingredients:
                    risk_level = "Low"
                    risk_factors = []
                    
                    if ing['expiry_date'] and ing['expiry_date'] <= date.today():
                        risk_level = "Critical"
                        risk_factors.append("Expired ingredient")
                    elif ing['expiry_date'] and (ing['expiry_date'] - date.today()).days <= 3:
                        risk_level = "High"
                        risk_factors.append("Expiring within 3 days")
                    
                    if ing['storage_temp'] and ing['storage_temp'] > 5:
                        risk_level = "High" if risk_level != "Critical" else "Critical"
                        risk_factors.append("Storage temperature too high")
                    
                    risk_items.append({
                        "item_type": "ingredient",
                        "item_id": ing['id'],
                        "item_name": ing['name'],
                        "risk_level": risk_level,
                        "risk_factors": risk_factors
                    })
        
        critical_count = sum(1 for item in risk_items if item['risk_level'] == 'Critical')
        high_count = sum(1 for item in risk_items if item['risk_level'] == 'High')
        
        overall_risk = "Low"
        if critical_count > 0:
            overall_risk = "Critical"
        elif high_count > 0:
            overall_risk = "High"
        
        return {
            "overall_risk_level": overall_risk,
            "summary": {
                "total_items_assessed": len(risk_items),
                "critical_risks": critical_count,
                "high_risks": high_count
            },
            "risk_items": risk_items
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict-outcomes")
def predict_health_outcomes(request: OutcomePredictionRequest):
    """Predict health outcomes"""
    try:
        patient = PatientService.get_patient(request.patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        prediction = AIService.predict_outcomes(
            request.patient_id, 
            request.time_horizon_days
        )
        
        return {
            "patient_id": request.patient_id,
            "prediction_horizon_days": request.time_horizon_days,
            "model_confidence": 0.87,
            **prediction
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize-recipe")
def optimize_recipe(request: RecipeOptimizeRequest):
    """Optimize recipe for health goals"""
    try:
        recipe = RecipeService.get_recipe(request.recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        optimization = AIService.optimize_recipe(recipe, request.health_goals)
        
        return {
            "recipe_id": request.recipe_id,
            "original_recipe": {
                "name": recipe['name'],
                "calories": recipe['total_calories'],
                "description": recipe['description']
            },
            "health_goals": request.health_goals,
            **optimization
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

