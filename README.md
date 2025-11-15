"""
# NutriGuard API - Modular FastAPI Backend

## 📁 Project Structure

```
nutriguard_api/
│
├── main.py                  # Application entry point
├── config.py                # Configuration settings
├── database.py              # Database connection
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
│
├── models/                  # Pydantic models
│   ├── patient.py
│   ├── recipe.py
│   ├── meal_plan.py
│   ├── ingredient.py
│   ├── safety.py
│   ├── nutrition.py
│   └── ai.py
│
├── routers/                 # API routes
│   ├── patients.py
│   ├── recipes.py
│   ├── meal_plans.py
│   ├── inventory.py
│   ├── safety.py
│   ├── compliance.py
│   ├── nutrition.py
│   ├── alerts.py
│   ├── ai.py
│   └── system.py
│
├── services/                # Business logic
│   ├── patient_service.py
│   ├── recipe_service.py
│   ├── meal_plan_service.py
│   ├── safety_service.py
│   ├── nutrition_service.py
│   └── ai_service.py
│
└── utils/                   # Utilities
    ├── enums.py
    └── helpers.py
```

## 🚀 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd nutriguard_api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Run the application**
```bash
python main.py
```

## 📚 API Documentation

Access the interactive API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔌 API Endpoints

### Patient Management
- `POST /patients` - Register new patient
- `GET /patients/{id}` - Get patient details
- `POST /patients/{id}/dietary-restrictions` - Update restrictions
- `GET /patients/{id}/nutrition-history` - View nutrition timeline
- `GET /patients/{id}/meal-plan` - Get current meal plan

### Meal Planning
- `POST /meal-plans/generate` - AI generates meal plan
- `POST /meal-plans/{id}/images` - Generate visual meal cards

### Recipe Management
- `GET /recipes/search` - Search recipes
- `POST /recipes` - Create new recipe
- `POST /recipes/{id}/modify` - AI modifies recipe

### Inventory
- `POST /inventory/ingredients` - Log ingredient delivery

### Food Safety
- `POST /safety/temperature-logs` - Record temperature
- `POST /safety/inspections` - Log safety inspection

### Compliance
- `GET /compliance/reports` - Generate compliance report

### Nutrition Monitoring
- `POST /nutrition/intake` - Log meal consumption
- `GET /nutrition/analytics/{patient_id}` - Get nutrition insights
- `POST /nutrition/analyze-correlation` - AI analyzes health outcomes

### Alerts
- `GET /alerts/dietary-violations` - Get compliance alerts

### AI Recommendations
- `POST /ai/recommend-meals` - Get meal recommendations
- `POST /ai/assess-risks` - Assess food safety risks
- `POST /ai/predict-outcomes` - Predict health outcomes
- `POST /ai/optimize-recipe` - Optimize recipe for health goals

### System
- `GET /` - API root information
- `GET /health` - Health check
- `GET /stats` - System statistics

## 🧪 Testing

Run the development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📝 Notes

- All AI endpoints use dummy data for demonstration
- Database triggers are automatically handled by PostgreSQL
- CORS is enabled for all origins (configure for production)
- All endpoints include proper error handling
""" AIService

router = APIRouter(prefix="/recipes", tags=["Recipe Management"])

@router.get("/search")
def search_recipes(keyword: str = None, max_calories: float = None):
    """Search recipes"""
    try:
        recipes = RecipeService.search_recipes(keyword, max_calories)
        return {"count": len(recipes), "recipes": recipes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", status_code=201)
def create_recipe(recipe: RecipeCreate):
    """Create new recipe"""
    try:
        result = RecipeService.create_recipe(recipe.dict())
        return {"message": "Recipe created", "recipe": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{recipe_id}/modify")
def modify_recipe(recipe_id: int, request: RecipeModifyRequest):
    """AI modifies recipe for dietary restrictions"""
    try:
        recipe = RecipeService.get_recipe(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        modifications = AIService.modify_recipe(recipe, request.dietary_requirements)
        return {
            "original_recipe": recipe,
            "dietary_requirements": request.dietary_requirements,
            **modifications
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== FILE: routers/meal_plans.py ====================
from fastapi import APIRouter, HTTPException
from services.meal_plan_service import MealPlanService
from services.patient_service import PatientService
from services.ai_service import
