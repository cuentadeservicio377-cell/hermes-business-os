"""
Skill: Ventas - Sales department
CRM, quotations, proposals, follow-ups
"""
from typing import Dict, Any, List
from app.skills.base import BaseSkill, action


class VentasSkill(BaseSkill):
    """Sales skill for managing clients, quotes, and proposals."""
    
    name = "ventas"
    description = "CRM, cotizaciones, propuestas y seguimiento de clientes"
    version = "1.0.0"
    
    def _register_actions(self) -> Dict[str, callable]:
        return {
            "crear_cliente": self.crear_cliente,
            "listar_clientes": self.listar_clientes,
            "crear_cotizacion": self.crear_cotizacion,
            "crear_propuesta": self.crear_propuesta,
            "seguimiento_cliente": self.seguimiento_cliente,
        }
    
    @action("Crear un nuevo cliente en el CRM")
    def crear_cliente(self, nombre: str, email: str = None, telefono: str = None, 
                      fuente: str = None, notas: str = None) -> Dict[str, Any]:
        """Create a new client in CRM."""
        return {
            "cliente": {
                "nombre": nombre,
                "email": email,
                "telefono": telefono,
                "fuente": fuente or "directo",
                "notas": notas,
                "estado": "lead"
            },
            "mensaje": f"Cliente '{nombre}' registrado exitosamente",
            "siguiente_paso": "Crear cotización o agregar a seguimiento"
        }
    
    @action("Listar todos los clientes")
    def listar_clientes(self, estado: str = None, limite: int = 50) -> Dict[str, Any]:
        """List clients with optional filtering."""
        # In real implementation, query database
        return {
            "filtro": estado or "todos",
            "limite": limite,
            "clientes": [],  # Would come from DB
            "mensaje": "Usa el dashboard para ver clientes completos"
        }
    
    @action("Crear cotización para un cliente")
    def crear_cotizacion(self, cliente: str, servicios: List[Dict], 
                         descuento: float = 0, notas: str = None) -> Dict[str, Any]:
        """Create a quotation for services."""
        subtotal = sum(s.get("precio", 0) * s.get("cantidad", 1) for s in servicios)
        descuento_monto = subtotal * (descuento / 100)
        total = subtotal - descuento_monto
        
        return {
            "cotizacion": {
                "cliente": cliente,
                "servicios": servicios,
                "subtotal": subtotal,
                "descuento": descuento_monto,
                "total": total,
                "moneda": "MXN",
                "notas": notas,
                "estado": "pendiente"
            },
            "mensaje": f"Cotización generada: ${total:,.2f} MXN",
            "siguiente_paso": "Enviar al cliente o convertir a proyecto"
        }
    
    @action("Crear propuesta formal de servicios")
    def crear_propuesta(self, cliente: str, alcance: str, precio: float, 
                        tiempos: str, entregables: List[str] = None) -> Dict[str, Any]:
        """Create a formal proposal with presentation."""
        return {
            "propuesta": {
                "cliente": cliente,
                "alcance": alcance,
                "inversion": precio,
                "tiempos": tiempos,
                "entregables": entregables or [],
                "formato": "slides"
            },
            "mensaje": f"Propuesta para {cliente} lista para presentar",
            "archivo": "propuesta_generada.pptx",
            "requiere_aprobacion": True
        }
    
    @action("Ver seguimiento de un cliente")
    def seguimiento_cliente(self, cliente: str) -> Dict[str, Any]:
        """Check follow-up status for a client."""
        return {
            "cliente": cliente,
            "ultimo_contacto": "2026-05-01",
            "proxima_accion": "Enviar cotización actualizada",
            "estado_pipeline": "negociacion",
            "dias_sin_contacto": 12,
            "alerta": "Cliente sin contacto por más de 7 días"
        }
