# ==================== FILE: models/ingredient.py ====================
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import date

class IngredientCreate(BaseModel):
    name: str
    nutritional_info: Optional[Dict[str, Any]] = None
    supplier: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    expiry_date: Optional[date] = None
    last_inspection_date: Optional[date] = None
    storage_temp: Optional[float] = None
