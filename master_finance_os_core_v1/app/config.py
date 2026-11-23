from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Master Finance OS Core"
    app_env: str = "development"
    host: str = "127.0.0.1"
    port: int = 8000
    database_path: str = "./data/mfos_core.db"
    ai_provider: str = "stub"
    ai_model: str = ""
    ai_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
