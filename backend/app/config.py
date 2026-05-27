import os


class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./ignitenow.db")
    admin_token: str = os.getenv("ADMIN_TOKEN", "demo-admin-token")
    static_base_url: str = os.getenv("STATIC_BASE_URL", "http://localhost:8000/static")
    jwt_secret: str = os.getenv("JWT_SECRET", "ignitenow-dev-secret")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "120"))


settings = Settings()
