from pydantic_settings import BaseSettings, SettingsConfigDict

class AuthSettings(BaseSettings):
    SECRET : str

    model_config = SettingsConfigDict(env_file=".env")

SECRET = AuthSettings().SECRET
