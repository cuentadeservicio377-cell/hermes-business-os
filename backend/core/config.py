"""
Hermes Business OS - Configuration
Loads settings from .env and client.yaml
"""
import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field
import yaml


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # App
    APP_NAME: str = "Hermes Business OS"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    # For SQLite, use absolute path to ensure it works regardless of CWD
    DATABASE_URL: str = Field(
        default=f"sqlite:///{Path(__file__).parent.parent.absolute()}/data/business.db", 
        env="DATABASE_URL"
    )
    
    # Security
    SECRET_KEY: str = Field(default="change-me-in-production", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # Integrations
    TELEGRAM_BOT_TOKEN: Optional[str] = Field(default=None, env="TELEGRAM_BOT_TOKEN")
    GOOGLE_SERVICE_ACCOUNT_JSON: Optional[str] = Field(default=None, env="GOOGLE_SERVICE_ACCOUNT_JSON")
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class ClientConfig:
    """Per-company configuration loaded from client.yaml."""
    
    def __init__(self, config_path: str = "config/client.yaml"):
        self.config_path = Path(config_path)
        self._config = {}
        self.load()
    
    def load(self):
        """Load configuration from YAML file."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
    
    @property
    def company(self) -> dict:
        return self._config.get("company", {})
    
    @property
    def departments(self) -> List[dict]:
        return self._config.get("departments", [])
    
    @property
    def integrations(self) -> dict:
        return self._config.get("integrations", {})
    
    @property
    def templates(self) -> dict:
        return self._config.get("templates", {})
    
    def get_department(self, name: str) -> Optional[dict]:
        """Get department config by name."""
        for dept in self.departments:
            if dept.get("name") == name:
                return dept
        return None
    
    def is_department_enabled(self, name: str) -> bool:
        """Check if a department is enabled."""
        dept = self.get_department(name)
        return dept.get("enabled", False) if dept else False


# Global instances
settings = Settings()
client_config = ClientConfig()
