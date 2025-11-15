# ==================== FILE: services/safety_service.py ====================
from database import get_db_connection
from psycopg2.extras import RealDictCursor

class SafetyService:
    
    @staticmethod
    def log_temperature(log_data: dict):
        """Log temperature reading"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Determine compliance
            temp = log_data['temperature']
            compliance = "Pass"
            if temp < 0 or temp > 5:
                compliance = "Warning"
            if temp > 10:
                compliance = "Fail"
            
            cursor.execute("""
                INSERT INTO safety_logs (ingredient_id, facility_area, temperature,
                                       inspector_id, compliance_status, remarks)
                VALUES (%(ingredient_id)s, %(facility_area)s, %(temperature)s,
                        %(inspector_id)s, %s, %(remarks)s)
                RETURNING *
            """, {**log_data, 'compliance_status': compliance})
            
            return dict(cursor.fetchone())
    
    @staticmethod
    def log_inspection(inspection_data: dict):
        """Log safety inspection"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
                INSERT INTO safety_logs (ingredient_id, facility_area, temperature,
                                       inspector_id, compliance_status, remarks,
                                       document_url)
                VALUES (%(ingredient_id)s, %(facility_area)s, %(temperature)s,
                        %(inspector_id)s, %(compliance_status)s, %(remarks)s,
                        %(document_url)s)
                RETURNING *
            """, inspection_data)
            
            result = dict(cursor.fetchone())
            
            # Create alert if failed
            if inspection_data['compliance_status'] == 'Fail':
                cursor.execute("""
                    INSERT INTO alerts (type, message, triggered_by)
                    VALUES (%s, %s, %s)
                """, ("Safety Violation",
                      f"Failed inspection in {inspection_data['facility_area']}",
                      inspection_data.get('inspector_id')))
            
            return result
    
    @staticmethod
    def get_compliance_report(start_date=None, end_date=None):
        """Generate compliance report"""
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = "SELECT * FROM safety_logs WHERE 1=1"
            params = []
            
            if start_date:
                query += " AND inspection_date >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND inspection_date <= %s"
                params.append(end_date)
            
            query += " ORDER BY inspection_date DESC"
            
            cursor.execute(query, params)
            logs = [dict(row) for row in cursor.fetchall()]
            
            # Calculate stats
            total = len(logs)
            passed = sum(1 for log in logs if log['compliance_status'] == 'Pass')
            failed = sum(1 for log in logs if log['compliance_status'] == 'Fail')
            warnings = sum(1 for log in logs if log['compliance_status'] == 'Warning')
            
            return {
                "total_inspections": total,
                "passed": passed,
                "failed": failed,
                "warnings": warnings,
                "compliance_rate": f"{(passed/total*100):.2f}%" if total > 0 else "N/A",
                "inspections": logs
            }
