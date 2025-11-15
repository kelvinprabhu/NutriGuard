# ==================== FILE: services/ai_agents/safety_inspector_agent.py ====================
"""Safety Inspection Agent - Assesses food safety risks"""

from langchain.prompts import PromptTemplate
from .base_agent import BaseAgent
from typing import Dict, Any, List
from datetime import date


class SafetyInspectorAgent(BaseAgent):
    """
    Specialized agent for food safety risk assessment
    Analyzes ingredients, storage conditions, and compliance
    """
    
    def __init__(self):
        super().__init__(temperature=0.05)  # Very low temp for safety-critical decisions
        self.prompt = PromptTemplate(
            input_variables=["ingredients_data", "facility_data", "recent_logs", "current_date"],
            template_format="jinja2",
            template="""
You are an expert food safety inspector and risk assessment AI specializing in healthcare facility food safety.

### Current Date:
{{ current_date }}

### Ingredients to Assess:
{{ ingredients_data }}

### Facility Areas:
{{ facility_data }}

### Recent Safety Logs:
{{ recent_logs }}

### Your Task:
Conduct a comprehensive food safety risk assessment.
Be CONSERVATIVE - err on the side of caution for patient safety.

### CRITICAL OUTPUT RULES:
- Output ONLY valid JSON
- NO markdown or extra text
- Be precise with risk levels and actionable recommendations

### Required JSON Structure:
{
  "assessment_timestamp": "2025-11-15T10:30:00",
  "overall_risk_level": "Low|Medium|High|Critical",
  "immediate_action_required": false,
  "summary": "Brief overview of assessment findings",
  "ingredient_assessments": [
    {
      "ingredient_id": 1,
      "ingredient_name": "Fresh Salmon",
      "risk_level": "High",
      "risk_factors": [
        {
          "factor": "Expiring in 2 days",
          "severity": "Medium",
          "impact": "Potential spoilage"
        },
        {
          "factor": "Storage temperature 7°C",
          "severity": "High",
          "impact": "Above safe refrigeration range"
        }
      ],
      "compliance_status": "Fail",
      "immediate_actions": [
        "Move to colder storage immediately",
        "Use within 24 hours or discard",
        "Do not serve to immunocompromised patients"
      ],
      "monitoring_frequency": "Every 4 hours"
    }
  ],
  "facility_assessments": [
    {
      "area": "Main Kitchen Refrigerator",
      "risk_level": "Medium",
      "temperature_status": {
        "current_avg": 5.5,
        "safe_range": "0-4°C",
        "status": "Above optimal"
      },
      "inspection_history": {
        "last_30_days_failures": 2,
        "compliance_rate": "93%"
      },
      "recommendations": [
        "Calibrate refrigerator thermostat",
        "Increase temperature monitoring to twice daily",
        "Review door seal integrity"
      ]
    }
  ],
  "critical_alerts": [],
  "compliance_summary": {
    "total_items_assessed": 15,
    "pass_count": 12,
    "warning_count": 2,
    "fail_count": 1,
    "overall_compliance_rate": "93.3%"
  },
  "risk_mitigation_plan": {
    "immediate_actions": [],
    "short_term_actions": [],
    "long_term_improvements": []
  },
  "regulatory_compliance": {
    "meets_fda_standards": true,
    "meets_local_regulations": true,
    "areas_of_concern": []
  },
  "follow_up_schedule": {
    "next_inspection_date": "2025-11-16",
    "special_monitoring_items": [],
    "documentation_requirements": []
  }
}
"""
        )
    
    def assess_safety_risks(self,
                           ingredients: List[Dict[str, Any]] = None,
                           facility_areas: List[str] = None,
                           recent_safety_logs: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Comprehensive food safety risk assessment
        
        Args:
            ingredients: List of ingredients to assess
            facility_areas: List of facility area names
            recent_safety_logs: Recent safety inspection logs
        
        Returns:
            Detailed risk assessment with actionable recommendations
        """
        current_date_str = date.today().isoformat()
        
        # Format ingredients
        if ingredients:
            ingredients_formatted = "\n".join([
                f"ID: {ing.get('id')}, Name: {ing.get('name')}, "
                f"Expiry: {ing.get('expiry_date')}, "
                f"Storage Temp: {ing.get('storage_temp')}°C, "
                f"Quantity: {ing.get('quantity')} {ing.get('unit')}, "
                f"Last Inspection: {ing.get('last_inspection_date')}"
                for ing in ingredients
            ])
        else:
            ingredients_formatted = "No specific ingredients to assess"
        
        # Format facility data (this would come from database)
        facility_formatted = "Standard facility areas" if not facility_areas else "\n".join(facility_areas)
        
        # Format recent logs
        if recent_safety_logs:
            logs_formatted = "\n".join([
                f"Date: {log.get('inspection_date')}, Area: {log.get('facility_area')}, "
                f"Status: {log.get('compliance_status')}, Temp: {log.get('temperature')}°C"
                for log in recent_safety_logs[-20:]  # Last 20 logs
            ])
        else:
            logs_formatted = "No recent safety logs available"
        
        result = self.invoke_with_search(
            self.prompt,
            {
                "ingredients_data": ingredients_formatted,
                "facility_data": facility_formatted,
                "recent_logs": logs_formatted,
                "current_date": current_date_str
            }
        )
        
        return result

