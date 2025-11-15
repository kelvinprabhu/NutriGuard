# ==================== FILE: routers/alerts.py ====================
from fastapi import APIRouter, HTTPException
from utils.enums import AlertStatus
from typing import Optional

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/dietary-violations")
def get_dietary_violations(status: Optional[AlertStatus] = None):
    """Get compliance alerts"""
    try:
        from database import get_db_connection
        from psycopg2.extras import RealDictCursor
        
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = "SELECT * FROM alerts WHERE 1=1"
            params = []
            
            if status:
                query += " AND status = %s"
                params.append(status.value)
            
            query += " ORDER BY created_at DESC LIMIT 50"
            
            cursor.execute(query, params)
            alerts = [dict(row) for row in cursor.fetchall()]
            
            return {"count": len(alerts), "alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

