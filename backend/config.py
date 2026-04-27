from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HR Assistant API"
    secret_key: str = "change-me-in-env"
    access_token_expire_minutes: int = 60 * 8
    algorithm: str = "HS256"

    sqlite_url: str = "sqlite:///./hr_assistant.db"
    vector_store_dir: str = "./data/vector_store"
    uploads_dir: str = "./data/uploads"

    gigachat_api_url: str = "https://gigachat.devices.sberbank.ru/api/v1"
    gigachat_auth_url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    gigachat_credentials: str = ""
    gigachat_scope: str = "GIGACHAT_API_PERS"
    gigachat_model: str = "GigaChat"
    embedding_model: str = "Embeddings"
    rag_top_k: int = 4

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
