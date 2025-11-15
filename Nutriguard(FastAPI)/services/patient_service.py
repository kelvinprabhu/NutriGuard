# ==================== FILE: services/patient_service.py ====================
from database import get_db_connection
from psycopg2.extras import RealDictCursor

class PatientService:
    
    @staticmethod
    def create_patient(patient_data: dict):
        """Create a new patient"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                INSERT INTO patients (name, age, gender, medical_conditions, 
                                    dietary_restrictions, admission_date, photo_url)
                VALUES (%(name)s, %(age)s, %(gender)s, %(medical_conditions)s,
                        %(dietary_restrictions)s, %(admission_date)s, %(photo_url)s)
                RETURNING *
            """, patient_data)
            return dict(cursor.fetchone())
    
    @staticmethod
    def get_patient(patient_id: int):
        """Get patient by ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def update_dietary_restrictions(patient_id: int, restrictions: str):
        """Update patient dietary restrictions"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                UPDATE patients 
                SET dietary_restrictions = %s, updated_at = NOW()
                WHERE id = %s
                RETURNING *
            """, (restrictions, patient_id))
            result = cursor.fetchone()
            return dict(result) if result else None
    
    @staticmethod
    def get_nutrition_history(patient_id: int, days: int = 30):
        """Get patient nutrition history"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                SELECT ne.*, r.name as recipe_name, r.total_calories,
                       s.name as recorded_by_name
                FROM nutrition_entries ne
                LEFT JOIN recipes r ON ne.recipe_id = r.id
                LEFT JOIN staff s ON ne.recorded_by = s.id
                WHERE ne.patient_id = %s 
                AND ne.date >= CURRENT_DATE - INTERVAL '%s days'
                ORDER BY ne.date DESC, ne.created_at DESC
            """, (patient_id, days))
            return [dict(row) for row in cursor.fetchall()]

