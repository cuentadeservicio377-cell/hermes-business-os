"""
Hermes Business OS — Kami Document Engine v3
Generates professional PDFs from HTML templates with dynamic variables.
"""

import re
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# WeasyPrint for PDF generation (optional)
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    from ...hermes_business_core.tools.config_loader import get_config
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "hermes-business-core" / "tools"))
    from config_loader import get_config


class KamiEngine:
    """
    Kami Document Engine v3.
    
    Generates professional documents from HTML templates with:
    - Dynamic variable substitution
    - Company branding (colors, logo)
    - Multi-format output (PDF, HTML)
    """
    
    def __init__(self):
        self.config = get_config()
        self.templates_dir = Path(__file__).parent.parent / "templates"
        
    def _get_template(self, template_name: str, industry: str = None) -> Optional[str]:
        """Find and load a template file."""
        if not industry:
            industry = self.config.industria
        
        # Try industry-specific template first
        paths = [
            self.templates_dir / industry / f"{template_name}.html",
            self.templates_dir / f"{template_name}.html",
            self.templates_dir / "default" / f"{template_name}.html",
        ]
        
        for path in paths:
            if path.exists():
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
        
        # Return default template
        return self._default_template(template_name)
    
    def _default_template(self, template_name: str) -> str:
        """Generate a minimal default template."""
        empresa = self.config.nombre
        color = self.config.get("empresa.branding.color_primario", "#2563EB")
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @page {{ size: letter; margin: 2.5cm; }}
        body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ border-bottom: 3px solid {color}; padding-bottom: 20px; margin-bottom: 30px; }}
        .header h1 {{ color: {color}; margin: 0; font-size: 28px; }}
        .header p {{ margin: 5px 0 0; color: #666; font-size: 14px; }}
        .content {{ margin: 30px 0; }}
        .footer {{ margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #999; text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: {color}; color: white; }}
        .total {{ font-size: 18px; font-weight: bold; color: {color}; text-align: right; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{{{{empresa.nombre}}}}</h1>
        <p>{{{{empresa.contacto.direccion}}}} | {{{{empresa.contacto.telefono}}}} | {{{{empresa.contacto.email}}}}</p>
    </div>
    
    <div class="content">
        <h2>{{{{documento.titulo}}}}</h2>
        <p><strong>Cliente:</strong> {{{{cliente.nombre}}}}</p>
        <p><strong>Fecha:</strong> {{{{fecha.hoy}}}}</p>
        <p><strong>Proyecto:</strong> {{{{proyecto.nombre}}}} ({{{{proyecto.id}}}})</p>
        
        <hr>
        
        {{{{documento.contenido}}}}
        
        <div class="total">Total: {{{{servicios.total}}}}</div>
    </div>
    
    <div class="footer">
        <p>{{{{empresa.nombre}}}} — Documento generado por Hermes Business OS</p>
        <p>{{{{fecha.hoy}}}}</p>
    </div>
</body>
</html>"""
    
    def _resolve_variables(self, template: str, variables: Dict[str, Any]) -> str:
        """Replace {{variable.path}} placeholders with actual values."""
        def replace_var(match):
            path = match.group(1).strip()
            value = self._get_nested_value(variables, path)
            return str(value) if value is not None else match.group(0)
        
        return re.sub(r"\{\{(.*?)\}\}", replace_var, template)
    
    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """Get a value from nested dict using dot notation."""
        keys = path.split(".")
        value = data
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return None
            else:
                return None
        
        return value
    
    def _build_variables(self, cliente: Dict[str, Any] = None, 
                        proyecto: Dict[str, Any] = None,
                        servicios: Any = None,
                        extras: Dict[str, Any] = None) -> Dict[str, Any]:
        """Build the complete variables dictionary."""
        now = datetime.now()
        
        variables = {
            "empresa": {
                "nombre": self.config.nombre,
                "industria": self.config.industria,
                "moneda": self.config.moneda,
                "contacto": self.config.get("empresa.contacto", {}),
                "branding": self.config.get("empresa.branding", {}),
            },
            "fecha": {
                "hoy": now.strftime("%d de %B de %Y"),
                "dia": now.day,
                "mes": now.strftime("%B"),
                "anio": now.year,
                "iso": now.strftime("%Y-%m-%d"),
            },
            "documento": {
                "titulo": "Documento",
                "contenido": "",
            },
            "cliente": cliente or {},
            "proyecto": proyecto or {},
            "servicios": servicios or {},
        }
        
        if extras:
            variables.update(extras)
        
        return variables
    
    def generate_pdf(self, template_name: str, output_path: str,
                     cliente: Dict[str, Any] = None,
                     proyecto: Dict[str, Any] = None,
                     servicios: Any = None,
                     extras: Dict[str, Any] = None) -> Optional[str]:
        """
        Generate a PDF document.
        
        Args:
            template_name: Name of the template (e.g., 'cotizacion-evento')
            output_path: Path to save the PDF
            cliente: Client data dict
            proyecto: Project data dict
            servicios: Services data (table or dict)
            extras: Additional variables
            
        Returns:
            Path to generated PDF or None on failure
        """
        if not WEASYPRINT_AVAILABLE:
            print("⚠️  WeasyPrint not installed. Install with: pip install weasyprint")
            # Fallback: save HTML instead
            html_path = output_path.replace(".pdf", ".html")
            return self.generate_html(template_name, html_path, cliente, proyecto, servicios, extras)
        
        # Load template
        template_html = self._get_template(template_name)
        if not template_html:
            return None
        
        # Build variables
        variables = self._build_variables(cliente, proyecto, servicios, extras)
        
        # Replace variables
        final_html = self._resolve_variables(template_html, variables)
        
        # Generate PDF
        try:
            html = HTML(string=final_html, base_url=str(self.templates_dir))
            html.write_pdf(output_path)
            return output_path
        except Exception as e:
            print(f"⚠️  Failed to generate PDF: {e}")
            return None
    
    def generate_html(self, template_name: str, output_path: str,
                      cliente: Dict[str, Any] = None,
                      proyecto: Dict[str, Any] = None,
                      servicios: Any = None,
                      extras: Dict[str, Any] = None) -> Optional[str]:
        """Generate an HTML document."""
        template_html = self._get_template(template_name)
        if not template_html:
            return None
        
        variables = self._build_variables(cliente, proyecto, servicios, extras)
        final_html = self._resolve_variables(template_html, variables)
        
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_html)
            return output_path
        except Exception as e:
            print(f"⚠️  Failed to generate HTML: {e}")
            return None
    
    def list_templates(self) -> list:
        """List available templates."""
        templates = []
        
        if self.templates_dir.exists():
            for path in self.templates_dir.rglob("*.html"):
                rel_path = path.relative_to(self.templates_dir)
                templates.append(str(rel_path.with_suffix("")))
        
        return sorted(templates)


# Singleton
_engine_instance = None


def get_kami_engine() -> KamiEngine:
    """Get or create singleton Kami engine instance."""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = KamiEngine()
    return _engine_instance
