from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME : str
    APP_VERSION : str
    ALLOWED_FILE_TYPES : list
    ALLOWED_FILE_SIZE : int
    CHUNK_SIZE : int
    MONGO_DB_URI : str
    MONGO_DB_NAME: str
    HUGGING_FACE_ACCESS_TOKEN: str
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )

def get_settings():
    return Settings()  # type: ignore[call-arg]