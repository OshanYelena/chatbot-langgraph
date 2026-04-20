from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # LLM
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/chatbot"
    redis_url: str = "redis://localhost:6379"

    # LangSmith
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""
    langchain_project: str = "chatbot-langgraph"

    # App
    app_env: str = "development"
    log_level: str = "INFO"
    secret_key: str = "change-me"


settings = Settings()
