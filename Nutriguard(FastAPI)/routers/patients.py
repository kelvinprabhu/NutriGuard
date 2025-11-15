# ==================== FILE: routers/patients.py ====================
from fastapi import APIRouter, HTTPException
from models.patient import PatientCreate, DietaryRestrictionUpdate
from services.patient_service import PatientService

router = APIRouter(prefix="/patients", tags=["Patient Management"])

@router.post("", status_code=201)
def register_patient(patient: PatientCreate):
    """Register new patient"""
    try:
        result = PatientService.create_patient(patient.dict())
        return {"message": "Patient registered successfully", "patient": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{patient_id}")
def get_patient(patient_id: int):
    """Get patient details"""
    try:
        patient = PatientService.get_patient(patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{patient_id}/dietary-restrictions")
def update_dietary_restrictions(patient_id: int, restrictions: DietaryRestrictionUpdate):
    """Update patient dietary restrictions"""
    try:
        result = PatientService.update_dietary_restrictions(
            patient_id, restrictions.dietary_restrictions
        )
        if not result:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"message": "Dietary restrictions updated", "patient": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{patient_id}/nutrition-history")
def get_nutrition_history(patient_id: int, days: int = 30):
    """View patient nutrition timeline"""
    try:
        history = PatientService.get_nutrition_history(patient_id, days)
        return {
            "patient_id": patient_id,
            "days": days,
            "entries": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{patient_id}/meal-plan")
def get_patient_meal_plan(patient_id: int):
    """Get current meal plan"""
    try:
        from services.meal_plan_service import MealPlanService
        meal_plan = MealPlanService.get_active_meal_plan(patient_id)
        
        if not meal_plan:
            return {"message": "No active meal plan found", "meal_plan": None}
        
        return meal_plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


