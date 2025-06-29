from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440 # 1 day
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    GIT_BRANCH: str = config("GIT_BRANCH")
    DOCKER_REPOSITORY: str = config("DOCKER_REPOSITORY")
    ROOT_PATH: str = config("ROOT_PATH")
    # QFaaS
    QFAAS_URL: str = config("QFAAS_URL")
    QFAAS_USER: str = config("QFAAS_USER")
    QFAAS_PASSWORD: str = config("QFAAS_PASSWORD")
    QFAAS_FUNCTION_URL: str = config("QFAAS_FUNCTION_URL")


settings = Settings()
