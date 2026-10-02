from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = 'sqlite:///./resume_skill_gap.db'
    SECRET_KEY: str = 'dev-secret-key'
    AI_API_KEY: str = ''
    CORS_ORIGINS: str = (
        'http://localhost:3000,http://localhost:3001,'
        'http://127.0.0.1:3000,http://127.0.0.1:3001,'
        'http://0.0.0.0:3000,http://0.0.0.0:3001'
    )

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
