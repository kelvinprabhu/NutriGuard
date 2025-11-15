from fastapi import APIRouter, HTTPException
from services.safety_service import SafetyService
from datetime import date
from typing import Optional

router = APIRouter(prefix="/compliance", tags=["Compliance"])

@router.get("/reports")
def generate_compliance_report(start_date: Optional[date] = None, end_date: Optional[date] = None):
    """Generate regulatory compliance report"""
    try:
        report = SafetyService.get_compliance_report(start_date, end_date)
        return {
            "report_period": {
                "start_date": start_date or "All time",
                "end_date": end_date or "Present"
            },
            "summary": {
                "total_inspections": report['total_inspections'],
                "passed": report['passed'],
                "failed": report['failed'],
                "warnings": report['warnings'],
                "compliance_rate": report['compliance_rate']
            },
            "inspections": report['inspections']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

