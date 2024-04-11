import os
from app.version import __version__


class Config:
    PROJECT_NAME = "EVS API"
    VERSION = __version__
    OPENAPI_URL = "/openapi.json"
    DOCS_URL = "/docs"
    REDOC_URL = "/redoc"
    SECRET_KEY = "your-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


class DevelopmentConfig(Config):
    DEBUG = True
    API_KEY = 'x-api-key'
    API_KEY_VALUE = 'test'
    POSTGRES_DATABASE_URL = "postgresql+psycopg2://postgres:evs!123@localhost:5432/evs"
    EXCLUDE_PATHS = ['/docs', '/redoc', '/openapi.json']


class ProductionConfig(Config):
    DEBUG = False
    API_KEY = os.getenv("API_KEY")
    API_KEY_VALUE = os.getenv("API_KEY_VALUE")
    POSTGRES_DATABASE_URL = os.getenv("POSTGRES_DATABASE_URL")
    EXCLUDE_PATHS = ['/docs', '/redoc']


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

settings = config[os.getenv("ENV", "development")]()
