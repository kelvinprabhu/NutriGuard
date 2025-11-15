# ==================== FILE: services/ai_service.py (UPDATED WITH REAL AGENTS) ====================
"""
AI Service - Integrated Multi-Agent System
Replaces dummy implementations with real AI agents
"""

from typing import Dict, Any, List, Optional
import logging
from .ai_agents.diet_planner_agent import DietPlannerAgent
from .ai_agents.recipe_modifier_agent import RecipeModifierAgent
from .ai_agents.nutrition_analyst_agent import NutritionAnalystAgent
from .ai_agents.safety_inspector_agent import SafetyInspectorAgent
from .ai_agents.outcome_predictor_agent import OutcomePredictorAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIService:
    """
    Main AI Service coordinating multiple specialized agents
    Each method delegates to the appropriate agent
    """
    
    def __init__(self):
        """Initialize all AI agents"""
        logger.info("Initializing AI Service with Multi-Agent System")
        
        try:
            self.diet_planner = DietPlannerAgent()
            self.recipe_modifier = RecipeModifierAgent()
            self.nutrition_analyst = NutritionAnalystAgent()
            self.safety_inspector = SafetyInspectorAgent()
            self.outcome_predictor = OutcomePredictorAgent()
            
            logger.info("✅ All AI agents initialized successfully")
        except Exception as e:
            logger.error(f"❌ Error initializing AI agents: {e}")
            raise
    
    @staticmethod
    def generate_meal_recommendations(patient_data: Dict[str, Any], 
                                     recipes_list: List[Dict[str, Any]] = None,
                                     dietitian_notes: Optional[str] = None,
                                     days: int = 1) -> Dict[str, Any]:
        """
        Generate personalized meal recommendations using Diet Planner Agent
        
        Args:
            patient_data: Patient medical and dietary information
            recipes_list: Available recipes to choose from
            dietitian_notes: Optional notes from dietitian
            days: Number of days for meal plan
        
        Returns:
            Comprehensive meal plan with nutritional analysis
        """
        try:
            logger.info(f"Generating meal plan for patient: {patient_data.get('name')}")
            
            # Initialize agent (lazy loading)
            agent = DietPlannerAgent()
            
            # Get recipes from database if not provided
            if recipes_list is None:
                from database import get_db_connection
                from psycopg2.extras import RealDictCursor
                
                with get_db_connection() as conn:
                    cursor = conn.cursor(cursor_factory=RealDictCursor)
                    cursor.execute("""
                        SELECT id, name, description, total_calories, image_url
                        FROM recipes
                        ORDER BY created_at DESC
                        LIMIT 50
                    """)
                    recipes_list = [dict(row) for row in cursor.fetchall()]
            
            # Generate meal plan
            result = agent.generate_meal_plan(
                patient_data=patient_data,
                recipes_list=recipes_list,
                dietitian_notes=dietitian_notes,
                days=days
            )
            
            logger.info("✅ Meal plan generated successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error generating meal recommendations: {e}")
            # Fallback to simple response if AI fails
            return {
                "error": str(e),
                "plan_summary": "Unable to generate AI meal plan. Please try again.",
                "recommended_meals": {
                    "breakfast": [{"name": "Oatmeal with fruits", "calories": 320}],
                    "lunch": [{"name": "Grilled chicken salad", "calories": 450}],
                    "dinner": [{"name": "Baked fish with vegetables", "calories": 420}]
                }
            }
    
    @staticmethod
    def modify_recipe(recipe_data: Dict[str, Any], 
                     requirements: List[str],
                     available_ingredients: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Modify recipe to meet dietary requirements using Recipe Modifier Agent
        
        Args:
            recipe_data: Original recipe information
            requirements: List of dietary restrictions/requirements
            available_ingredients: Optional list of available ingredients
        
        Returns:
            Modified recipe with substitutions and nutritional updates
        """
        try:
            logger.info(f"Modifying recipe: {recipe_data.get('name')}")
            
            agent = RecipeModifierAgent()
            
            # Get available ingredients if not provided
            if available_ingredients is None:
                from database import get_db_connection
                from psycopg2.extras import RealDictCursor
                
                with get_db_connection() as conn:
                    cursor = conn.cursor(cursor_factory=RealDictCursor)
                    cursor.execute("""
                        SELECT name, quantity, unit, expiry_date
                        FROM ingredients
                        WHERE expiry_date > CURRENT_DATE
                        AND quantity > 0
                        LIMIT 100
                    """)
                    available_ingredients = [dict(row) for row in cursor.fetchall()]
            
            result = agent.modify_recipe(
                recipe_data=recipe_data,
                dietary_requirements=requirements,
                available_ingredients=available_ingredients
            )
            
            logger.info("✅ Recipe modified successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error modifying recipe: {e}")
            return {
                "error": str(e),
                "can_modify": False,
                "modifications": [
                    {"change": "Reduce sodium", "impact": "Lower salt content"},
                    {"change": "Increase fiber", "impact": "Add whole grains"}
                ],
                "modified_recipe": {
                    "name": f"{recipe_data['name']} (Modified)",
                    "total_calories": recipe_data.get('total_calories', 0) * 0.85
                }
            }
    
    @staticmethod
    def assess_risks(ingredients: List[Dict[str, Any]] = None,
                    areas: List[str] = None,
                    recent_logs: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Assess food safety risks using Safety Inspector Agent
        
        Args:
            ingredients: List of ingredients to assess
            areas: List of facility areas
            recent_logs: Recent safety logs
        
        Returns:
            Comprehensive safety risk assessment
        """
        try:
            logger.info("Conducting food safety risk assessment")
            
            agent = SafetyInspectorAgent()
            
            # Get data from database if not provided
            if ingredients is None and areas is None:
                from database import get_db_connection
                from psycopg2.extras import RealDictCursor
                
                with get_db_connection() as conn:
                    cursor = conn.cursor(cursor_factory=RealDictCursor)
                    
                    # Get recent ingredients
                    cursor.execute("""
                        SELECT id, name, expiry_date, storage_temp, quantity, unit, last_inspection_date
                        FROM ingredients
                        WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
                        LIMIT 50
                    """)
                    ingredients = [dict(row) for row in cursor.fetchall()]
                    
                    # Get recent safety logs
                    cursor.execute("""
                        SELECT facility_area, temperature, compliance_status, 
                               inspection_date, remarks
                        FROM safety_logs
                        ORDER BY inspection_date DESC
                        LIMIT 50
                    """)
                    recent_logs = [dict(row) for row in cursor.fetchall()]
            
            result = agent.assess_safety_risks(
                ingredients=ingredients,
                facility_areas=areas,
                recent_safety_logs=recent_logs
            )
            
            logger.info("✅ Safety assessment completed")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error assessing risks: {e}")
            return {
                "error": str(e),
                "overall_risk_level": "Unknown",
                "risk_items": [],
                "recommendations": [
                    "Continue regular monitoring",
                    "Conduct manual inspection"
                ]
            }
    
    @staticmethod
    def predict_outcomes(patient_id: int, 
                        meal_plan_id: Optional[int] = None,
                        time_horizon: int = 30) -> Dict[str, Any]:
        """
        Predict health outcomes using Outcome Predictor Agent
        
        Args:
            patient_id: Patient ID
            meal_plan_id: Optional meal plan ID
            time_horizon: Prediction timeframe in days
        
        Returns:
            Health outcome predictions with confidence intervals
        """
        try:
            logger.info(f"Predicting outcomes for patient {patient_id}")
            
            from database import get_db_connection
            from psycopg2.extras import RealDictCursor
            
            # Get patient data
            with get_db_connection() as conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                
                cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
                patient_data = dict(cursor.fetchone())
                
                # Get meal plan
                if meal_plan_id:
                    cursor.execute("""
                        SELECT * FROM meal_plans WHERE id = %s
                    """, (meal_plan_id,))
                    meal_plan = dict(cursor.fetchone())
                else:
                    cursor.execute("""
                        SELECT * FROM meal_plans 
                        WHERE patient_id = %s 
                        ORDER BY created_at DESC 
                        LIMIT 1
                    """, (patient_id,))
                    result = cursor.fetchone()
                    meal_plan = dict(result) if result else {}
                
                # Get historical nutrition data
                cursor.execute("""
                    SELECT date, intake_percentage, blood_sugar, notes
                    FROM nutrition_entries
                    WHERE patient_id = %s
                    ORDER BY date DESC
                    LIMIT 90
                """, (patient_id,))
                historical_data = [dict(row) for row in cursor.fetchall()]
            
            agent = OutcomePredictorAgent()
            
            result = agent.predict_outcomes(
                patient_data=patient_data,
                meal_plan=meal_plan,
                historical_data=historical_data,
                time_horizon_days=time_horizon
            )
            
            logger.info("✅ Outcome prediction completed")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error predicting outcomes: {e}")
            return {
                "error": str(e),
                "predictions": {
                    "blood_sugar_control": {
                        "trend": "Stable",
                        "confidence": "Low"
                    }
                },
                "recommendations": [
                    "Continue monitoring",
                    "Consult with healthcare provider"
                ]
            }
    
    @staticmethod
    def optimize_recipe(recipe_data: Dict[str, Any], 
                       health_goals: List[str]) -> Dict[str, Any]:
        """
        Optimize recipe for health goals (uses Recipe Modifier Agent)
        
        Args:
            recipe_data: Recipe to optimize
            health_goals: List of health goals
        
        Returns:
            Optimized recipe with improvements
        """
        try:
            logger.info(f"Optimizing recipe: {recipe_data.get('name')}")
            
            # Convert health goals to dietary requirements
            requirements = []
            for goal in health_goals:
                if "sodium" in goal.lower():
                    requirements.append("Low sodium")
                if "fiber" in goal.lower():
                    requirements.append("High fiber")
                if "glycemic" in goal.lower() or "sugar" in goal.lower():
                    requirements.append("Low glycemic index")
                if "protein" in goal.lower():
                    requirements.append("High protein")
                if "fat" in goal.lower():
                    requirements.append("Low saturated fat")
            
            # Use recipe modifier agent
            agent = RecipeModifierAgent()
            result = agent.modify_recipe(
                recipe_data=recipe_data,
                dietary_requirements=requirements
            )
            
            # Reformat for optimization response
            if result.get("can_modify"):
                optimized = {
                    "optimizations": result.get("modifications_made", []),
                    "health_score": result.get("health_score_improvement", {}),
                    "optimized_recipe": result.get("modified_recipe", {}),
                    "suitability": result.get("dietary_compliance", {})
                }
            else:
                optimized = {
                    "error": "Recipe cannot be optimized for these goals",
                    "optimizations": [],
                    "health_score": {"original": 6.5, "optimized": 6.5}
                }
            
            logger.info("✅ Recipe optimization completed")
            return optimized
            
        except Exception as e:
            logger.error(f"❌ Error optimizing recipe: {e}")
            return {
                "error": str(e),
                "optimizations": [
                    {"goal": "General health", "changes": ["Use fresh ingredients"]}
                ],
                "health_score": {"original": 6.5, "optimized": 7.0}
            }
    
    @staticmethod
    def analyze_nutrition_correlation(patient_id: int,
                                     analysis_period_days: int = 30) -> Dict[str, Any]:
        """
        Analyze correlation between nutrition and health outcomes
        
        Args:
            patient_id: Patient ID
            analysis_period_days: Days to analyze
        
        Returns:
            Correlation analysis with insights
        """
        try:
            logger.info(f"Analyzing nutrition correlation for patient {patient_id}")
            
            from database import get_db_connection
            from psycopg2.extras import RealDictCursor
            
            with get_db_connection() as conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                
                # Get patient data
                cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
                patient_data = dict(cursor.fetchone())
                
                # Get nutrition entries
                cursor.execute("""
                    SELECT ne.*, r.name as recipe_name, r.total_calories
                    FROM nutrition_entries ne
                    LEFT JOIN recipes r ON ne.recipe_id = r.id
                    WHERE ne.patient_id = %s
                    AND ne.date >= CURRENT_DATE - INTERVAL '%s days'
                    ORDER BY ne.date DESC
                """, (patient_id, analysis_period_days))
                nutrition_entries = [dict(row) for row in cursor.fetchall()]
            
            agent = NutritionAnalystAgent()
            
            result = agent.analyze_correlation(
                patient_data=patient_data,
                nutrition_entries=nutrition_entries,
                analysis_period_days=analysis_period_days
            )
            
            logger.info("✅ Correlation analysis completed")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error analyzing correlation: {e}")
            return {
                "error": str(e),
                "analysis_summary": "Unable to complete analysis",
                "correlations_found": [],
                "recommendations": ["Ensure consistent data logging"]
            }

