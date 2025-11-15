from datetime import date, timedelta

def calculate_date_range(days: int = 30):
    """Calculate start and end date for given days"""
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date