"""
Hermes Business OS — Cotizador Tool
Generates professional quotes/cotizaciones with pricing logic.
"""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "hermes-business-core" / "tools"))

from config_loader import get_config


class Cotizador:
    """Quote/estimate generator with pricing logic."""
    
    def __init__(self):
        self.config = get_config()
        self.data_dir = Path(__file__).parent.parent.parent.parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.quotes_file = self.data_dir / "quotes.json"
        self.catalog_file = self.data_dir / "catalog.json"
        self._quotes = None
        self._catalog = None
        self._next_quote_num = 1
        
    def _load_catalog(self) -> Dict[str, Any]:
        """Load service/product catalog."""
        if self._catalog is not None:
            return self._catalog
        
        if self.catalog_file.exists():
            try:
                with open(self.catalog_file, "r", encoding="utf-8") as f:
                    self._catalog = json.load(f)
                    return self._catalog
            except Exception:
                pass
        
        # Default catalog by industry
        self._catalog = self._default_catalog()
        return self._catalog
    
    def _default_catalog(self) -> Dict[str, Any]:
        """Generate default catalog based on industry."""
        industry = self.config.industria
        moneda = self.config.moneda
        
        catalogs = {
            "eventos": {
                "servicios": [
                    {"codigo": "EVT-BAS", "nombre": "Paquete Básico", "descripcion": "Decoración básica para evento", "precio_base": 50000, "unidad": "evento"},
                    {"codigo": "EVT-INT", "nombre": "Paquete Intermedio", "descripcion": "Decoración intermedia + mobiliario", "precio_base": 100000, "unidad": "evento"},
                    {"codigo": "EVT-PRE", "nombre": "Paquete Premium", "descripcion": "Decoración premium + mobiliario + iluminación", "precio_base": 180000, "unidad": "evento"},
                    {"codigo": "EVT-MES", "nombre": "Mesas de dulces", "descripcion": "Mesa de dulces personalizada", "precio_base": 8000, "unidad": "mesa"},
                    {"codigo": "EVT-FLO", "nombre": "Arreglo floral", "descripcion": "Centros de mesa y decoración floral", "precio_base": 5000, "unidad": "arreglo"},
                ],
                "multiplicadores": {
                    "temporada_alta": 1.2,
                    "temporada_baja": 0.9,
                    "urgencia": 1.3,
                    "fin_de_semana": 1.0,
                }
            },
            "legal": {
                "servicios": [
                    {"codigo": "LEG-CON", "nombre": "Revisión de contrato", "descripcion": "Revisión y opinión legal de contrato", "precio_base": 15000, "unidad": "contrato"},
                    {"codigo": "LEG-DEM", "nombre": "Elaboración de demanda", "descripcion": "Demanda civil o mercantil", "precio_base": 35000, "unidad": "demanda"},
                    {"codigo": "LEG-ASE", "nombre": "Asesoría mensual", "descripcion": "Asesoría legal mensual preventiva", "precio_base": 12000, "unidad": "mes"},
                    {"codigo": "LEG-REP", "nombre": "Representación judicial", "descripcion": "Representación en juicio", "precio_base": 50000, "unidad": "juicio"},
                    {"codigo": "LEG-CONS", "nombre": "Consulta legal", "descripcion": "Consulta puntual", "precio_base": 3000, "unidad": "consulta"},
                ],
                "multiplicadores": {
                    "complejidad_alta": 1.5,
                    "complejidad_media": 1.2,
                    "urgencia": 1.3,
                }
            },
            "consultoria": {
                "servicios": [
                    {"codigo": "CON-DIA", "nombre": "Diagnóstico", "descripcion": "Diagnóstico inicial de negocio", "precio_base": 25000, "unidad": "diagnóstico"},
                    {"codigo": "CON-EST", "nombre": "Estrategia", "descripcion": "Plan estratégico", "precio_base": 50000, "unidad": "plan"},
                    {"codigo": "CON-IMP", "nombre": "Implementación", "descripcion": "Implementación de estrategia", "precio_base": 40000, "unidad": "mes"},
                    {"codigo": "CON-CAP", "nombre": "Capacitación", "descripcion": "Taller o capacitación", "precio_base": 15000, "unidad": "sesión"},
                ],
                "multiplicadores": {
                    "empresa_grande": 1.5,
                    "empresa_mediana": 1.2,
                    "urgencia": 1.2,
                }
            },
            "retail": {
                "servicios": [
                    {"codigo": "RTL-PRO", "nombre": "Producto A", "descripcion": "Descripción del producto", "precio_base": 500, "unidad": "pieza"},
                    {"codigo": "RTL-PRB", "nombre": "Producto B", "descripcion": "Descripción del producto", "precio_base": 800, "unidad": "pieza"},
                    {"codigo": "RTL-ENV", "nombre": "Envío", "descripcion": "Envío a domicilio", "precio_base": 150, "unidad": "envío"},
                ],
                "multiplicadores": {
                    "mayoreo": 0.85,
                    "menudeo": 1.0,
                }
            },
        }
        
        return catalogs.get(industry, catalogs["consultoria"])
    
    def _load_quotes(self) -> List[Dict[str, Any]]:
        """Load existing quotes."""
        if self._quotes is not None:
            return self._quotes
        
        if self.quotes_file.exists():
            try:
                with open(self.quotes_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._quotes = data.get("quotes", [])
                    self._next_quote_num = data.get("next_num", 1)
                    return self._quotes
            except Exception:
                pass
        
        self._quotes = []
        self._next_quote_num = 1
        return self._quotes
    
    def _save_quotes(self):
        """Save quotes to JSON."""
        data = {
            "quotes": self._quotes,
            "next_num": self._next_quote_num,
            "updated_at": datetime.now().isoformat(),
        }
        with open(self.quotes_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _generate_quote_id(self) -> str:
        """Generate quote ID (COT-001, COT-002, etc.)."""
        quote_id = f"COT-{self._next_quote_num:03d}"
        self._next_quote_num += 1
        return quote_id
    
    def list_services(self) -> List[Dict[str, Any]]:
        """List available services from catalog."""
        catalog = self._load_catalog()
        return catalog.get("servicios", [])
    
    def find_service(self, query: str) -> Optional[Dict[str, Any]]:
        """Find a service by code or name."""
        services = self.list_services()
        query_lower = query.lower()
        
        for service in services:
            if query_lower == service["codigo"].lower():
                return service
            if query_lower in service["nombre"].lower():
                return service
        
        return None
    
    def calculate_quote(self, servicios: List[Dict[str, Any]], 
                       multiplicadores: List[str] = None,
                       descuento: float = 0) -> Dict[str, Any]:
        """
        Calculate quote totals.
        
        Args:
            servicios: List of {codigo, cantidad, descripcion} or service dicts
            multiplicadores: List of multiplier keys to apply
            descuento: Discount percentage (0-100)
        
        Returns:
            Quote calculation breakdown
        """
        catalog = self._load_catalog()
        catalog_services = {s["codigo"]: s for s in catalog.get("servicios", [])}
        multipliers = catalog.get("multiplicadores", {})
        moneda = self.config.moneda
        
        line_items = []
        subtotal = 0
        
        for item in servicios:
            if isinstance(item, dict) and "codigo" in item:
                codigo = item["codigo"]
                cantidad = item.get("cantidad", 1)
                custom_desc = item.get("descripcion")
            else:
                codigo = item
                cantidad = 1
                custom_desc = None
            
            service = catalog_services.get(codigo)
            if not service:
                continue
            
            precio_unitario = service["precio_base"]
            descripcion = custom_desc or service["descripcion"]
            
            total_linea = precio_unitario * cantidad
            subtotal += total_linea
            
            line_items.append({
                "codigo": codigo,
                "nombre": service["nombre"],
                "descripcion": descripcion,
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "total_linea": total_linea,
                "unidad": service["unidad"],
            })
        
        # Apply multipliers
        factor = 1.0
        if multiplicadores:
            for mult in multiplicadores:
                if mult in multipliers:
                    factor *= multipliers[mult]
        
        subtotal_multiplicado = subtotal * factor
        
        # Apply discount
        descuento_monto = subtotal_multiplicado * (descuento / 100)
        subtotal_con_descuento = subtotal_multiplicado - descuento_monto
        
        # Calculate IVA
        iva_porcentaje = self.config.get("documentos.iva_porcentaje", 16)
        iva_incluido = self.config.get("documentos.iva_incluido", True)
        
        if iva_incluido:
            total = subtotal_con_descuento
            subtotal_sin_iva = total / (1 + iva_porcentaje / 100)
            iva_monto = total - subtotal_sin_iva
        else:
            subtotal_sin_iva = subtotal_con_descuento
            iva_monto = subtotal_sin_iva * (iva_porcentaje / 100)
            total = subtotal_sin_iva + iva_monto
        
        return {
            "line_items": line_items,
            "subtotal": round(subtotal, 2),
            "factor_multiplicador": round(factor, 2),
            "subtotal_con_multiplicador": round(subtotal_multiplicado, 2),
            "descuento_porcentaje": descuento,
            "descuento_monto": round(descuento_monto, 2),
            "subtotal_neto": round(subtotal_con_descuento, 2),
            "iva_porcentaje": iva_porcentaje,
            "iva_monto": round(iva_monto, 2),
            "iva_incluido": iva_incluido,
            "total": round(total, 2),
            "moneda": moneda,
        }
    
    def create_quote(self, cliente_id: str, cliente_nombre: str,
                    servicios: List[Dict[str, Any]],
                    proyecto_nombre: str = None,
                    multiplicadores: List[str] = None,
                    descuento: float = 0,
                    notas: str = None,
                    validez_dias: int = 15) -> Dict[str, Any]:
        """
        Create a new quote.
        
        Returns the created quote dict.
        """
        self._load_quotes()
        
        calculo = self.calculate_quote(servicios, multiplicadores, descuento)
        
        quote = {
            "id": self._generate_quote_id(),
            "cliente_id": cliente_id,
            "cliente_nombre": cliente_nombre,
            "proyecto_nombre": proyecto_nombre or f"Proyecto {cliente_nombre}",
            "fecha_creacion": datetime.now().isoformat(),
            "fecha_vencimiento": (datetime.now() + timedelta(days=validez_dias)).isoformat(),
            "validez_dias": validez_dias,
            "estado": "borrador",
            "version": 1,
            "servicios": servicios,
            "calculo": calculo,
            "notas": notas or "",
            "aprobada": False,
            "fecha_aprobacion": None,
        }
        
        self._quotes.append(quote)
        self._save_quotes()
        
        return {
            "success": True,
            "cotizacion": quote,
            "message": f"Cotización {quote['id']} creada para {cliente_nombre}",
        }
    
    def get_quote(self, quote_id: str) -> Optional[Dict[str, Any]]:
        """Get quote by ID."""
        self._load_quotes()
        
        for quote in self._quotes:
            if quote["id"].lower() == quote_id.lower():
                return quote
        
        return None
    
    def approve_quote(self, quote_id: str) -> Dict[str, Any]:
        """Approve a quote."""
        self._load_quotes()
        
        for quote in self._quotes:
            if quote["id"].lower() == quote_id.lower():
                quote["estado"] = "aprobada"
                quote["aprobada"] = True
                quote["fecha_aprobacion"] = datetime.now().isoformat()
                self._save_quotes()
                
                return {
                    "success": True,
                    "cotizacion": quote,
                    "message": f"Cotización {quote_id} aprobada",
                }
        
        return {
            "success": False,
            "error": f"Cotización {quote_id} no encontrada",
        }
    
    def format_quote_text(self, quote: Dict[str, Any]) -> str:
        """Format quote for display in conversation."""
        calc = quote["calculo"]
        moneda = calc["moneda"]
        
        lines = [
            f"📋 **Cotización {quote['id']}**",
            f"Cliente: {quote['cliente_nombre']}",
            f"Proyecto: {quote['proyecto_nombre']}",
            f"Fecha: {quote['fecha_creacion'][:10]}",
            f"Válida por: {quote['validez_dias']} días",
            "",
            "**Servicios:**",
        ]
        
        for item in calc["line_items"]:
            lines.append(f"• {item['nombre']} x{item['cantidad']} = {moneda} {item['total_linea']:,.2f}")
        
        lines.extend([
            "",
            f"Subtotal: {moneda} {calc['subtotal']:,.2f}",
        ])
        
        if calc["factor_multiplicador"] != 1.0:
            lines.append(f"Ajustes: x{calc['factor_multiplicador']}")
        
        if calc["descuento_porcentaje"] > 0:
            lines.append(f"Descuento: {calc['descuento_porcentaje']}% (-{moneda} {calc['descuento_monto']:,.2f})")
        
        lines.extend([
            f"Subtotal neto: {moneda} {calc['subtotal_neto']:,.2f}",
            f"IVA ({calc['iva_porcentaje']}%): {moneda} {calc['iva_monto']:,.2f}",
            f"**TOTAL: {moneda} {calc['total']:,.2f}**",
            "",
            f"Estado: {quote['estado'].upper()}",
        ])
        
        return "\n".join(lines)


# Singleton
_cotizador_instance = None


def get_cotizador() -> Cotizador:
    """Get or create singleton Cotizador instance."""
    global _cotizador_instance
    if _cotizador_instance is None:
        _cotizador_instance = Cotizador()
    return _cotizador_instance
