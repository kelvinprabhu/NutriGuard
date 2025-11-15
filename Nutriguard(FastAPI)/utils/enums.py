from enum import Enum

class StaffRole(str, Enum):
    ADMIN = "Admin"
    DIETITIAN = "Dietitian"
    NURSE = "Nurse"
    KITCHEN_STAFF = "KitchenStaff"

class MealType(str, Enum):
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    SNACK = "Snack"

class ComplianceStatus(str, Enum):
    PASS = "Pass"
    FAIL = "Fail"
    WARNING = "Warning"

class AlertStatus(str, Enum):
    ACTIVE = "Active"
    RESOLVED = "Resolved"
