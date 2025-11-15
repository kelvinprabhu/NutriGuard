# ==================== FILE: services/nutrition_service.py ====================
from database import get_db_connection
from psycopg2.extras import RealDictCursor
from datetime import date

class NutritionService:
    
    @staticmethod
    def log_intake(intake_data: dict):
        """Log nutrition intake"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            if 'date' not in intake_data or intake_data['date'] is None:
                intake_data['date'] = date.today()
            
            cursor.execute("""
                INSERT INTO nutrition_entries (patient_id, recipe_id, recorded_by,
                                             date, intake_percentage, blood_sugar, notes)
                VALUES (%(patient_id)s, %(recipe_id)s, %(recorded_by)s,
                        %(date)s, %(intake_percentage)s, %(blood_sugar)s, %(notes)s)
                RETURNING *
            """, intake_data)
            
            result = dict(cursor.fetchone())
            
            # Check for violations
            if intake_data.get('intake_percentage') and intake_data['intake_percentage'] < 50:
                cursor.execute("""
                    INSERT INTO alerts (type, message, triggered_by)
                    VALUES (%s, %s, %s)
                """, ("Low Intake",
                      f"Patient {intake_data['patient_id']} consumed less than 50% of meal",
                      intake_data.get('recorded_by')))
            
            return result
    
    @staticmethod
    def get_analytics(patient_id: int, days: int = 30):
        """Get nutrition analytics"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT ne.*, r.total_calories
                FROM nutrition_entries ne
                LEFT JOIN recipes r ON ne.recipe_id = r.id
                WHERE ne.patient_id = %s 
                AND ne.date >= CURRENT_DATE - INTERVAL '%s days'
                ORDER BY ne.date DESC
            """, (patient_id, days))
            
            entries = [dict(row) for row in cursor.fetchall()]
            
            if not entries:
                return None
            
            # Calculate stats
            total_entries = len(entries)
            avg_intake = sum(e['intake_percentage'] or 0 for e in entries) / total_entries
            
            blood_sugar_entries = [e for e in entries if e.get('blood_sugar')]
            avg_blood_sugar = sum(e['blood_sugar'] for e in blood_sugar_entries) / len(blood_sugar_entries) if blood_sugar_entries else 0
            
            total_calories = sum(
                (e['total_calories'] or 0) * ((e['intake_percentage'] or 100) / 100)
                for e in entries
            )
            
            return {
                "total_meals_logged": total_entries,
                "average_intake_percentage": round(avg_intake, 2),
                "average_blood_sugar": round(avg_blood_sugar, 2),
                "total_calories_consumed": round(total_calories, 2),
                "daily_average_calories": round(total_calories / days, 2),
                "recent_entries": entries[:10]
            }
