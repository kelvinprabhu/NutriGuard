from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database Configuration
    DB_NAME: str = "nutriguard"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "1234"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    
    # API Configuration
    API_TITLE: str = "NutriGuard API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Healthcare Food Management System"
    
    class Config:
        env_file = ".env"

settings = Settings()