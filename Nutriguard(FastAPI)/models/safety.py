# ==================== FILE: models/safety.py ====================
from pydantic import BaseModel
from typing import Optional
from utils.enums import ComplianceStatus

class TemperatureLog(BaseModel):
    facility_area: str
    temperature: float
    inspector_id: Optional[int] = None
    ingredient_id: Optional[int] = None
    remarks: Optional[str] = None

class SafetyInspection(BaseModel):
    ingredient_id: Optional[int] = None
    facility_area: str
    temperature: Optional[float] = None
    inspector_id: Optional[int] = None
    compliance_status: ComplianceStatus
    remarks: Optional[str] = None
    document_url: Optional[str] = None


