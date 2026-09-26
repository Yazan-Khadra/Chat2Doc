from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME : str
    APP_VERSION : str
    ALLOWED_FILE_TYPES : list
    ALLOWED_FILE_SIZE : int
    CHUNK_SIZE : int

    model_config = SettingsConfigDict(
        env_file=".env"
    )

def get_settings():
    return Settings()