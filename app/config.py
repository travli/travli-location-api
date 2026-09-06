from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "travli-location-api"
    app_env: str = "development"
    port: int = 8000

    geoapify_api_key: str
    redis_url: str = "redis://localhost:6380"
    redis_ttl: int = 3600

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
