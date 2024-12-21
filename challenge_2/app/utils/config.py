from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    supabase_url: str
    supabase_key: str
    database_url: str
    vector_store_path: str = "./vector_db"

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()