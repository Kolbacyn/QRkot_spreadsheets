from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'FastAPI app for charity project'
    description: str = 'It was lot of fun'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'p@ssw0rd'
    token_lifetime: int = 3600
    password_min_length: int = 3
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
