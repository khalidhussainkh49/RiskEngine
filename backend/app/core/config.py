from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "NCDIPS"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/ncdips"
    REDIS_URL: str = "redis://redis:6379/0"
    SECRET_KEY: str = "super-secret-key-change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 1 week

    NEO4J_URI: str = "bolt://neo4j:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"

    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"

    class Config:
        env_file = ".env"

settings = Settings()
