# ==================== FILE: routers/system.py ====================
from fastapi import APIRouter, HTTPException
from datetime import datetime

router = APIRouter(prefix="", tags=["System"])

@router.get("/")
def root():
    """API Root endpoint"""
    return {
        "service": "NutriGuard API",
        "version": "1.0.0",
        "description": "Healthcare Food Management System",
        "documentation": "/docs",
        "endpoints": {
            "patient_management": "/patients",
            "meal_planning": "/meal-plans",
            "recipes": "/recipes",
            "inventory": "/inventory",
            "safety": "/safety",
            "compliance": "/compliance",
            "nutrition": "/nutrition",
            "alerts": "/alerts",
            "ai": "/ai"
        }
    }

@router.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        from database import get_db_connection
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            return {
                "status": "healthy",
                "database": "connected",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/stats")
def get_system_stats():
    """Get system statistics"""
    try:
        from database import get_db_connection
        from psycopg2.extras import RealDictCursor
        
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("SELECT COUNT(*) as count FROM patients")
            patients_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM recipes")
            recipes_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM meal_plans")
            meal_plans_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM ingredients")
            ingredients_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM safety_logs")
            safety_logs_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM alerts WHERE status = 'Active'")
            active_alerts_count = cursor.fetchone()['count']
            
            return {
                "system_stats": {
                    "patients": patients_count,
                    "recipes": recipes_count,
                    "meal_plans": meal_plans_count,
                    "ingredients": ingredients_count,
                    "safety_logs": safety_logs_count,
                    "active_alerts": active_alerts_count
                },
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

