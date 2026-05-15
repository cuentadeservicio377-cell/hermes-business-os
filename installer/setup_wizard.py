"""
Hermes Business OS — Setup Wizard
Interactive onboarding to configure a new company.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, Any


class SetupWizard:
    """Interactive setup wizard for new HBOS installations."""
    
    INDUSTRIES = [
        ("eventos", "Eventos y celebraciones (bodas, fiestas, corporativos)"),
        ("legal", "Servicios legales (despachos, consultoría jurídica)"),
        ("retail", "Retail y comercio (tiendas, e-commerce)"),
        ("consultoria", "Consultoría profesional (marketing, diseño, IT)"),
        ("salud", "Salud y bienestar (clínicas, spa, fitness)"),
        ("tecnologia", "Tecnología y software"),
        ("otro", "Otra industria"),
    ]
    
    SIZES = [
        ("solopreneur", "Soy solo yo (1 persona)"),
        ("pequena", "2-10 empleados"),
        ("mediana", "11-50 empleados"),
    ]
    
    def __init__(self, non_interactive: bool = False):
        self.non_interactive = non_interactive
        self.hbos_path = Path(__file__).parent.parent
        self.config_path = self.hbos_path / "config" / "empresa.yaml"
        self.data: Dict[str, Any] = {}
        
    def run(self):
        """Run the setup wizard."""
        print("\n" + "=" * 50)
        print("🏢  Hermes Business OS — Setup Wizard")
        print("=" * 50)
        print("\n¡Bienvenido! Voy a ayudarte a configurar Hermes para tu empresa.")
        print("Este proceso toma unos 5-10 minutos.\n")
        
        if self.non_interactive:
            self._generate_default_config()
        else:
            self._interactive_setup()
        
        self._save_config()
        self._show_summary()
        
        print("\n✅ Setup complete!")
        print("\nNext steps:")
        print("  1. Review your config: config/empresa.yaml")
        print("  2. Set up Google Workspace integration (optional)")
        print("  3. Start Hermes: hermes gateway start")
        print("  4. Talk to your bot on Telegram!")
    
    def _interactive_setup(self):
        """Run interactive prompts."""
        # Company name
        self.data["nombre"] = self._ask(
            "¿Cuál es el nombre de tu empresa?",
            validator=lambda x: len(x) > 0,
            error_msg="El nombre no puede estar vacío."
        )
        
        # Industry
        print("\n¿A qué industria pertenece tu empresa?")
        for i, (key, desc) in enumerate(self.INDUSTRIES, 1):
            print(f"  {i}. {desc}")
        
        choice = self._ask_choice("Selecciona una opción", len(self.INDUSTRIES))
        self.data["industria"] = self.INDUSTRIES[choice - 1][0]
        
        # Size
        print("\n¿De qué tamaño es tu equipo?")
        for i, (key, desc) in enumerate(self.SIZES, 1):
            print(f"  {i}. {desc}")
        
        choice = self._ask_choice("Selecciona una opción", len(self.SIZES))
        self.data["tamano"] = self.SIZES[choice - 1][0]
        
        # Currency
        print("\n¿Qué moneda usas principalmente?")
        print("  1. MXN (Peso mexicano)")
        print("  2. USD (Dólar estadounidense)")
        print("  3. EUR (Euro)")
        print("  4. COP (Peso colombiano)")
        print("  5. ARS (Peso argentino)")
        print("  6. Otra")
        
        currencies = ["MXN", "USD", "EUR", "COP", "ARS", "OTHER"]
        choice = self._ask_choice("Selecciona una opción", 6)
        self.data["moneda"] = currencies[choice - 1]
        if self.data["moneda"] == "OTHER":
            self.data["moneda"] = self._ask("Escribe el código de tu moneda (ej: PEN, CLP):").upper()
        
        # Departments
        print("\n¿Qué departamentos necesitas activar?")
        deps = {
            "ventas": "Ventas (CRM, cotizaciones, seguimiento)",
            "operaciones": "Operaciones (proyectos, tareas, checklists)",
            "documentos": "Documentos (contratos, reportes, propuestas)",
            "finanzas": "Finanzas (presupuestos, pagos, reportes) 🚧",
            "rrhh": "RRHH (nómina, equipos, asistencia) 🚧",
        }
        
        self.data["departamentos"] = {}
        for key, desc in deps.items():
            resp = self._ask(f"¿Activar {desc}? (s/n)", default="s" if key in ["ventas", "operaciones", "documentos"] else "n")
            self.data["departamentos"][key] = {"activo": resp.lower() in ("s", "si", "sí", "y", "yes")}
        
        # Contact
        print("\nDatos de contacto (opcionales, para documentos):")
        self.data["contacto"] = {
            "email": self._ask("Email de la empresa (opcional):", required=False) or None,
            "telefono": self._ask("Teléfono (opcional):", required=False) or None,
            "direccion": self._ask("Dirección (opcional):", required=False) or None,
        }
        
        # Branding
        print("\nBranding (opcional):")
        color = self._ask("Color primario en hex (ej: #2563EB) o dejar vacío:", required=False)
        self.data["branding"] = {
            "color_primario": color if color else "#2563EB",
            "logo_url": None,
        }
    
    def _ask(self, prompt: str, validator=None, error_msg="Entrada inválida.", default=None, required=True) -> str:
        """Ask user for input with validation."""
        while True:
            if default:
                full_prompt = f"{prompt} [{default}]: "
            else:
                full_prompt = f"{prompt}: "
            
            response = input(full_prompt).strip()
            
            if not response and default:
                return default
            
            if not response and not required:
                return ""
            
            if not response and required:
                print("  ⚠️  Este campo es obligatorio.")
                continue
            
            if validator and not validator(response):
                print(f"  ⚠️  {error_msg}")
                continue
            
            return response
    
    def _ask_choice(self, prompt: str, max_choice: int) -> int:
        """Ask for a numeric choice."""
        while True:
            try:
                response = input(f"{prompt}: ").strip()
                choice = int(response)
                if 1 <= choice <= max_choice:
                    return choice
                print(f"  ⚠️  Selecciona un número entre 1 y {max_choice}.")
            except ValueError:
                print("  ⚠️  Ingresa un número válido.")
    
    def _generate_default_config(self):
        """Generate default config for non-interactive mode."""
        self.data = {
            "nombre": "Mi Empresa",
            "industria": "consultoria",
            "tamano": "pequena",
            "moneda": "MXN",
            "departamentos": {
                "ventas": {"activo": True},
                "operaciones": {"activo": True},
                "documentos": {"activo": True},
                "finanzas": {"activo": False},
                "rrhh": {"activo": False},
            },
            "contacto": {
                "email": None,
                "telefono": None,
                "direccion": None,
            },
            "branding": {
                "color_primario": "#2563EB",
                "logo_url": None,
            },
        }
    
    def _save_config(self):
        """Save configuration to YAML file."""
        config = {
            "empresa": {
                "nombre": self.data["nombre"],
                "industria": self.data["industria"],
                "tamano": self.data["tamano"],
                "moneda": self.data["moneda"],
                "idioma": "es",
                "timezone": "America/Mexico_City",
                "contacto": self.data.get("contacto", {}),
                "branding": self.data.get("branding", {}),
            },
            "departamentos": {},
            "integraciones": {
                "google_workspace": {
                    "activo": False,
                    "cuenta_servicio": "config/google-service-account.json",
                    "carpeta_drive": f"Hermes OS — {self.data['nombre']}",
                    "spreadsheet_maestro": "Indice de Proyectos",
                },
                "telegram": {"activo": True},
                "calendario": {"activo": False, "proveedor": "google"},
            },
        }
        
        # Add department configs
        for dept, settings in self.data.get("departamentos", {}).items():
            config["departamentos"][dept] = {
                "activo": settings.get("activo", False),
            }
        
        # Ensure config directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
        
        print(f"\n💾 Config saved to: {self.config_path}")
    
    def _show_summary(self):
        """Show configuration summary."""
        print("\n" + "=" * 50)
        print("📋  Resumen de Configuración")
        print("=" * 50)
        print(f"  Empresa: {self.data['nombre']}")
        print(f"  Industria: {self.data['industria']}")
        print(f"  Tamaño: {self.data['tamano']}")
        print(f"  Moneda: {self.data['moneda']}")
        print(f"\n  Departamentos activos:")
        for dept, settings in self.data.get("departamentos", {}).items():
            status = "✅" if settings.get("activo") else "❌"
            print(f"    {status} {dept}")
        print()


if __name__ == "__main__":
    wizard = SetupWizard()
    wizard.run()
