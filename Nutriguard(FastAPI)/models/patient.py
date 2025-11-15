from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class PatientCreate(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    medical_conditions: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    admission_date: Optional[date] = None
    photo_url: Optional[str] = None

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    medical_conditions: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    photo_url: Optional[str] = None

class DietaryRestrictionUpdate(BaseModel):
    dietary_restrictions: str

class PatientResponse(BaseModel):
    id: int
    name: str
    age: Optional[int]
    gender: Optional[str]
    medical_conditions: Optional[str]
    dietary_restrictions: Optional[str]


