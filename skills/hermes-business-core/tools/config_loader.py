"""
Hermes Business OS — Config Loader
Loads and validates empresa.yaml configuration.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigLoader:
    """Loads and provides access to company configuration."""
    
    def __init__(self, config_path: str = None):
        if config_path:
            self.config_path = Path(config_path)
        else:
            # Try to find config relative to skills directory
            self.config_path = self._find_config()
        
        self._config: Optional[Dict[str, Any]] = None
        self._load()
    
    def _find_config(self) -> Path:
        """Find config/empresa.yaml in the project."""
        # Start from this file's location and go up
        current = Path(__file__).resolve()
        
        # Go up: tools -> hermes-business-core -> skills -> project_root
        for parent in [current.parent.parent.parent.parent, current.parent.parent.parent]:
            config_file = parent / "config" / "empresa.yaml"
            if config_file.exists():
                return config_file
        
        # Fallback to current directory
        return Path("config/empresa.yaml")
    
    def _load(self):
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            self._config = self._default_config()
            return
        
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️  Error loading config: {e}")
            self._config = self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "empresa": {
                "nombre": "Mi Empresa",
                "industria": "consultoria",
                "tamano": "pequena",
                "moneda": "MXN",
                "idioma": "es",
                "timezone": "America/Mexico_City",
            },
            "departamentos": {
                "ventas": {"activo": True},
                "operaciones": {"activo": True},
                "documentos": {"activo": True},
                "finanzas": {"activo": False},
                "rrhh": {"activo": False},
            },
            "integraciones": {
                "google_workspace": {"activo": False},
                "telegram": {"activo": True},
            },
        }
    
    @property
    def empresa(self) -> Dict[str, Any]:
        """Get empresa section."""
        return self._config.get("empresa", {})
    
    @property
    def nombre(self) -> str:
        return self.empresa.get("nombre", "Mi Empresa")
    
    @property
    def industria(self) -> str:
        return self.empresa.get("industria", "consultoria")
    
    @property
    def tamano(self) -> str:
        return self.empresa.get("tamano", "pequena")
    
    @property
    def moneda(self) -> str:
        return self.empresa.get("moneda", "MXN")
    
    @property
    def departamentos(self) -> Dict[str, Any]:
        return self._config.get("departamentos", {})
    
    def departamento_activo(self, nombre: str) -> bool:
        """Check if a department is active."""
        dept = self.departamentos.get(nombre, {})
        return dept.get("activo", False)
    
    @property
    def integraciones(self) -> Dict[str, Any]:
        return self._config.get("integraciones", {})
    
    def integracion_activa(self, nombre: str) -> bool:
        """Check if an integration is active."""
        integration = self.integraciones.get(nombre, {})
        return integration.get("activo", False)
    
    def get(self, path: str, default=None):
        """Get a value by dot-notation path (e.g., 'empresa.nombre')."""
        keys = path.split(".")
        value = self._config
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default


# Singleton instance
_config_instance = None


def get_config() -> ConfigLoader:
    """Get or create singleton config instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader()
    return _config_instance
