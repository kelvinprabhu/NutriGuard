from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings

# Import routers
from routers import (
    patients,
    recipes,
    meal_plans,
    inventory,
    safety,
    compliance,
    nutrition,
    alerts,
    ai,
    system
)

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(system.router)
app.include_router(patients.router)
app.include_router(recipes.router)
app.include_router(meal_plans.router)
app.include_router(inventory.router)
app.include_router(safety.router)
app.include_router(compliance.router)
app.include_router(nutrition.router)
app.include_router(alerts.router)
app.include_router(ai.router)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

