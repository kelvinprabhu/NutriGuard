# NutriGuard - Healthcare Food Management System

## 🎯 Project Overview

**NutriGuard** is an AI-powered healthcare food management system for hospitals and healthcare facilities. It manages patient nutrition, meal planning, food safety, and compliance tracking through intelligent automation.

**Core Purpose:** Automate nutrition management for hospital patients with medical conditions (diabetes, hypertension, allergies) through AI-driven meal planning and safety monitoring.

---

## 🛠️ Technical Stack

### **Backend**
- **Framework:** FastAPI 0.104.1
- **Language:** Python 3.9+
- **Server:** Uvicorn (ASGI)
- **Architecture:** Multi-agent AI system with modular services

### **Database**
- **RDBMS:** PostgreSQL 14+
- **Schema:** `nutriguard` with 9 core tables
- **ORM:** Raw SQL with psycopg2
- **Connection:** Context manager pattern with connection pooling

### **AI/ML Stack**
- **LLM:** Google Gemini 2.0 Flash
- **Framework:** LangChain
- **API:** Google Generative AI API
- **Architecture:** 5 specialized AI agents

### **API**
- **Style:** RESTful
- **Documentation:** OpenAPI 3.0 (Swagger UI)
- **Format:** JSON
- **CORS:** Enabled for all origins

---

## 📁 Project Structure

```
nutriguard_api/
├── main.py                      # FastAPI app initialization & router registration
├── config.py                    # Environment configuration (Pydantic Settings)
├── database.py                  # PostgreSQL connection management
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (gitignored)
│
├── models/                      # Pydantic validation models
│   ├── __init__.py
│   ├── patient.py              # Patient schemas
│   ├── recipe.py               # Recipe schemas
│   ├── meal_plan.py            # Meal plan schemas
│   ├── ingredient.py           # Ingredient schemas
│   ├── safety.py               # Safety inspection schemas
│   ├── nutrition.py            # Nutrition entry schemas
│   └── ai.py                   # AI request/response schemas
│
├── routers/                     # API endpoints (controllers)
│   ├── __init__.py
│   ├── patients.py             # Patient management (5 endpoints)
│   ├── recipes.py              # Recipe management (3 endpoints)
│   ├── meal_plans.py           # Meal planning (9 endpoints)
│   ├── inventory.py            # Inventory management (1 endpoint)
│   ├── safety.py               # Food safety (2 endpoints)
│   ├── compliance.py           # Compliance reports (1 endpoint)
│   ├── nutrition.py            # Nutrition monitoring (3 endpoints)
│   ├── alerts.py               # Alert system (2 endpoints)
│   ├── ai.py                   # AI recommendations (4 endpoints)
│   └── system.py               # System utilities (3 endpoints)
│
├── services/                    # Business logic layer
│   ├── __init__.py
│   ├── patient_service.py      # Patient CRUD operations
│   ├── recipe_service.py       # Recipe CRUD operations
│   ├── meal_plan_service.py    # Meal plan operations
│   ├── safety_service.py       # Safety inspection logic
│   ├── nutrition_service.py    # Nutrition analytics
│   ├── ai_service.py           # AI service coordinator
│   │
│   └── ai_agents/              # Multi-agent AI system
│       ├── __init__.py
│       ├── base_agent.py       # Base agent with LLM integration
│       ├── diet_planner_agent.py      # Meal planning AI
│       ├── recipe_modifier_agent.py   # Recipe modification AI
│       ├── nutrition_analyst_agent.py # Nutrition analysis AI
│       ├── safety_inspector_agent.py  # Food safety AI
│       └── outcome_predictor_agent.py # Health prediction AI
│
└── utils/                       # Shared utilities
    ├── __init__.py
    ├── enums.py                # Enums (StaffRole, MealType, etc.)
    └── helpers.py              # Helper functions
```

---

## 🗄️ Database Schema

### **Core Tables (9)**

**1. staff** - Healthcare staff (admins, dietitians, nurses)
```sql
id, name, email, password_hash, role, certification, is_active
```

**2. patients** - Patient records
```sql
id, name, age, gender, medical_conditions, dietary_restrictions, admission_date, photo_url
```

**3. ingredients** - Food inventory
```sql
id, name, nutritional_info (JSONB), supplier, quantity, unit, expiry_date, storage_temp
```

**4. recipes** - Recipe database
```sql
id, name, description, image_url, total_calories, created_by
```

**5. meal_plans** - Patient meal plans
```sql
id, patient_id, created_by, start_date, end_date, ai_generated, notes
```

**6. nutrition_entries** - Daily nutrition logs
```sql
id, patient_id, recipe_id, date, intake_percentage, blood_sugar, notes
```

**7. safety_logs** - Food safety inspections
```sql
id, ingredient_id, facility_area, temperature, compliance_status, remarks
```

**8. alerts** - System alerts
```sql
id, type, message, triggered_by, status (Active/Resolved)
```

**9. Bridge Tables:**
- `recipe_ingredients` - Recipe-Ingredient mapping
- `meal_plan_recipes` - MealPlan-Recipe mapping with meal_type

### **Triggers**
- Auto-update `updated_at` timestamps
- Auto-generate alerts for expired ingredients
- Auto-generate alerts for low intake violations

---

## 🤖 Multi-Agent AI System

### **Architecture Pattern:** Specialized Agent Pattern

Each agent is a single-purpose AI that excels at one task. The `AIService` coordinates between agents.

### **5 AI Agents:**

#### **1. DietPlannerAgent**
**Purpose:** Generate personalized meal plans
**Input:**
- Patient medical data (conditions, restrictions)
- Available recipes
- Dietitian notes
- Plan duration (1-7 days)

**Output:**
```json
{
  "plan_summary": "...",
  "daily_nutritional_targets": {...},
  "meals": {
    "breakfast": {...},
    "mid_morning_snack": {...},
    "lunch": {...},
    "evening_snack": {...},
    "dinner": {...}
  },
  "used_recipe_ids": [1, 2, 3],
  "special_considerations": [...],
  "suggested_new_recipes": [...]
}
```

**Key Features:**
- Medical condition awareness
- Recipe reuse optimization
- Indian cuisine support
- Calorie/macro calculations

---

#### **2. RecipeModifierAgent**
**Purpose:** Adapt recipes for dietary restrictions
**Input:**
- Original recipe
- Dietary requirements (low sodium, diabetic, etc.)
- Available ingredients

**Output:**
```json
{
  "can_modify": true,
  "modified_recipe": {
    "ingredients": [{
      "original": "white rice",
      "replacement": "quinoa",
      "reason": "Lower glycemic index"
    }],
    "nutritional_info": {...}
  },
  "modifications_made": [...],
  "health_score_improvement": {
    "original": 6.5,
    "optimized": 8.7,
    "improvement_percentage": 34
  }
}
```

**Key Features:**
- Smart ingredient substitution
- Nutritional recalculation
- Cultural authenticity preservation
- Health scoring

---

#### **3. NutritionAnalystAgent**
**Purpose:** Analyze nutrition data & correlations
**Input:**
- Patient info
- 30-90 days of nutrition entries
- Blood sugar readings

**Output:**
```json
{
  "correlations_found": [
    {
      "factor": "High carb meals",
      "health_metric": "Blood sugar",
      "correlation_strength": "Strong positive",
      "average_impact": "+18 mg/dL",
      "recommendation": "..."
    }
  ],
  "trends": {...},
  "best_performing_meals": [...],
  "meals_to_modify": [...]
}
```

**Key Features:**
- Pattern recognition
- Trend analysis
- Evidence-based recommendations
- Risk identification

---

#### **4. SafetyInspectorAgent**
**Purpose:** Food safety risk assessment
**Input:**
- Ingredient data (expiry, temp, storage)
- Facility areas
- Recent inspection logs

**Output:**
```json
{
  "overall_risk_level": "Low|Medium|High|Critical",
  "ingredient_assessments": [
    {
      "ingredient_id": 1,
      "risk_level": "High",
      "risk_factors": [...],
      "immediate_actions": [...]
    }
  ],
  "compliance_summary": {...},
  "follow_up_schedule": {...}
}
```

**Key Features:**
- Conservative risk assessment
- FDA/regulatory compliance
- Immediate action alerts
- Temperature monitoring

---

#### **5. OutcomePredictorAgent**
**Purpose:** Predict health outcomes
**Input:**
- Patient data
- Current meal plan
- Historical nutrition data (90 days)
- Prediction timeframe (30 days)

**Output:**
```json
{
  "predicted_outcomes": {
    "blood_sugar_control": {
      "current_average": 128.5,
      "predicted_average": 118.2,
      "confidence_interval": {"lower": 115, "upper": 121.5},
      "trend": "Improving"
    },
    "weight_management": {...}
  },
  "risk_factors": {...},
  "milestone_predictions": {...}
}
```

**Key Features:**
- Time-series prediction
- Confidence intervals
- Milestone tracking
- Risk mitigation

---

## 🔌 API Endpoints (33 Total)

### **Patient Management (5)**
```
POST   /patients                          # Register patient
GET    /patients/{id}                     # Get patient details
POST   /patients/{id}/dietary-restrictions # Update restrictions
GET    /patients/{id}/meal-plan           # Get active meal plan
GET    /patients/{id}/nutrition-history   # Get nutrition timeline
```

### **Recipe Management (3)**
```
POST   /recipes                           # Create recipe
GET    /recipes/search                    # Search recipes
POST   /recipes/{id}/modify               # AI modify recipe
```

### **Meal Planning (9)**
```
POST   /meal-plans/generate               # AI generate plan
GET    /meal-plans/{id}                   # Get meal plan
POST   /meal-plans/{id}/images            # Generate meal cards
POST   /meal-plans/{id}/recipes           # Add recipe to plan
DELETE /meal-plans/{id}/recipes/{rid}    # Remove recipe
GET    /meal-plans/patient/{id}/active    # Get active plans
GET    /meal-plans/patient/{id}/history   # Get plan history
PUT    /meal-plans/{id}                   # Update meal plan
DELETE /meal-plans/{id}                   # Delete meal plan
```

### **Inventory (1)**
```
POST   /inventory/ingredients             # Log ingredient
```

### **Food Safety (2)**
```
POST   /safety/temperature-logs           # Log temperature
POST   /safety/inspections                # Log inspection
```

### **Compliance (1)**
```
GET    /compliance/reports                # Generate report
```

### **Nutrition Monitoring (3)**
```
POST   /nutrition/intake                  # Log intake
GET    /nutrition/analytics/{id}          # Get analytics
POST   /nutrition/analyze-correlation     # AI correlation
```

### **Alerts (2)**
```
GET    /alerts/dietary-violations         # Get alerts
```

### **AI Recommendations (4)**
```
POST   /ai/recommend-meals                # AI meal recommendations
POST   /ai/assess-risks                   # AI risk assessment
POST   /ai/predict-outcomes               # AI outcome prediction
POST   /ai/optimize-recipe                # AI recipe optimization
```

### **System (3)**
```
GET    /                                  # API info
GET    /health                            # Health check
GET    /stats                             # System stats
```

---

## 🚀 Setup & Installation

### **1. Prerequisites**
```bash
Python 3.9+
PostgreSQL 14+
Google AI API Key
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
langchain==0.1.0
langchain-google-genai==1.0.0
google-generativeai==0.3.0
```

### **3. Database Setup**
```bash
# Create database
psql -U postgres -c "CREATE DATABASE nutriguard;"

# Run schema
psql -U postgres -d nutriguard -f schema.sql
```

### **4. Environment Configuration**
Create `.env` file:
```env
DB_NAME=nutriguard
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

GOOGLE_AI_API_KEY=your_api_key_here
```

### **5. Run Application**
```bash
python main.py
# Server runs on http://localhost:8000
```

### **6. Access Documentation**
```
Swagger UI: http://localhost:8000/docs
ReDoc:      http://localhost:8000/redoc
```

---

## 🔄 Request/Response Flow

### **Example: Generate Meal Plan**

**1. Client Request:**
```http
POST /meal-plans/generate?patient_id=1&days=7
```

**2. Flow:**
```
Router (meal_plans.py)
  ↓
AIService.generate_meal_recommendations()
  ↓
Fetch patient data from DB
  ↓
Fetch available recipes from DB
  ↓
DietPlannerAgent.generate_meal_plan()
  ↓
Gemini API call with structured prompt
  ↓
Parse JSON response
  ↓
Create meal_plan record in DB
  ↓
Return to client
```

**3. Response:**
```json
{
  "message": "Meal plan generated successfully",
  "meal_plan": {
    "id": 15,
    "patient_id": 1,
    "start_date": "2025-11-22",
    "end_date": "2025-11-29",
    "ai_generated": true
  },
  "ai_recommendations": {
    "plan_summary": "...",
    "meals": {...},
    "nutritional_targets": {...}
  }
}
```

---

## 🧪 Testing

### **Using Postman**
1. Import `NutriGuard_Collection.json`
2. Set variables: `base_url`, `patient_id`, `recipe_id`
3. Run collection or individual requests

### **Test Workflow**
```
1. Health Check → /health
2. Register Patient → POST /patients
3. Create Recipes → POST /recipes
4. Generate Meal Plan → POST /meal-plans/generate
5. Log Nutrition → POST /nutrition/intake
6. Get Analytics → GET /nutrition/analytics/{id}
```

---

## 📊 Key Features Implementation

### **1. AI Meal Planning**
- **Tech:** LangChain + Gemini 2.0 Flash
- **Prompt:** Jinja2 template with patient context
- **Output:** Structured JSON with nutritional targets
- **Fallback:** Pre-defined healthy meals if AI fails

### **2. Real-time Safety Monitoring**
- **Triggers:** PostgreSQL triggers for alerts
- **Temperature:** Automated compliance checks
- **Expiry:** Auto-alert for items expiring <3 days

### **3. Nutrition Analytics**
- **Data:** 30-90 day windows
- **Analysis:** Blood sugar vs meal correlations
- **Visualization:** Trends, best/worst meals

### **4. Error Handling**
- **Database:** Connection pooling, retry logic
- **AI:** Fallback responses, error logging
- **Validation:** Pydantic models at API layer

---

## 🔐 Security Considerations

**Implemented:**
- Environment variables for secrets
- Password hashing (placeholder in schema)
- SQL injection prevention (parameterized queries)

**Not Implemented (Production TODO):**
- JWT authentication
- Role-based access control (RBAC)
- HTTPS/SSL
- Rate limiting
- API key management

---

## 📈 Performance

**Database:**
- Indexed columns: patient names, ingredient expiry, recipe names
- Connection pooling via context managers

**API:**
- Async-ready (ASGI with Uvicorn)
- Lazy agent initialization
- Database query optimization

**AI:**
- Response caching (future enhancement)
- Temperature=0.1 for consistency
- Max retries: 3

---

## 🛣️ Future Enhancements

1. **Authentication:** JWT + OAuth2
2. **Caching:** Redis for AI responses
3. **Async DB:** SQLAlchemy async ORM
4. **WebSockets:** Real-time alerts
5. **Image Analysis:** Meal photo analysis with vision AI
6. **Mobile App:** React Native client
7. **Reporting:** PDF generation for compliance
8. **Multi-language:** i18n support

---

## 📞 API Testing Examples

### **Quick Test Commands**

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Register Patient:**
```bash
curl -X POST http://localhost:8000/patients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 65,
    "medical_conditions": "Type 2 Diabetes",
    "dietary_restrictions": "Low sodium"
  }'
```

**Generate Meal Plan:**
```bash
curl -X POST "http://localhost:8000/meal-plans/generate?patient_id=1&days=7"
```

---

## 📝 License & Credits

**Project:** NutriGuard Healthcare Food Management System
**Architecture:** Modular FastAPI with Multi-Agent AI
**AI Model:** Google Gemini 2.0 Flash
**Database:** PostgreSQL 14+

---

**Documentation Version:** 1.0
**Last Updated:** November 2025
