# ==================== FILE: routers/safety.py ====================
from fastapi import APIRouter, HTTPException
from models.safety import TemperatureLog, SafetyInspection
from services.safety_service import SafetyService
from datetime import date
from typing import Optional

router = APIRouter(prefix="/safety", tags=["Food Safety"])

@router.post("/temperature-logs", status_code=201)
def record_temperature(log: TemperatureLog):
    """Record temperature reading"""
    try:
        result = SafetyService.log_temperature(log.dict())
        return {"message": "Temperature logged", "log": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/inspections", status_code=201)
def log_inspection(inspection: SafetyInspection):
    """Log safety inspection"""
    try:
        data = inspection.dict()
        data['compliance_status'] = inspection.compliance_status.value
        result = SafetyService.log_inspection(data)
        return {"message": "Inspection logged", "inspection": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

