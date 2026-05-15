"""
Hermes Business OS — Intent Router
Routes user messages to the appropriate department skill.
"""

import re
from typing import Optional, Dict, Any
try:
    from .config_loader import get_config
except ImportError:
    from config_loader import get_config


class IntentRouter:
    """Routes natural language intents to department skills."""
    
    # Keyword mappings for intent detection
    INTENT_PATTERNS = {
        "hermes-ventas": {
            "keywords": [
                "cliente", "prospecto", "lead", "cotiz", "cotiza", "precio", "costo",
                "propuesta", "contrato", "venta", "vender", "pipeline", "funnel",
                "seguimiento", "seguir", "llamar", "contactar", "honorarios",
                "factur", "factura", "pago recibido", "anticipo",
            ],
            "patterns": [
                r"\b(registra|nuevo|agrega)\s+(un\s+)?cliente",
                r"\bcotiza\w*\b",
                r"\bpropuesta\b",
                r"\bpipeline\b",
                r"\bseguimiento\b",
            ]
        },
        "hermes-operaciones": {
            "keywords": [
                "proyecto", "tarea", "pendiente", "checklist", "timeline",
                "produccion", "ejecucion", "entrega", "hito", "deadline",
                "fecha", "calendario", "agenda", "recordatorio",
                "asignar", "responsable", "equipo", "staff",
            ],
            "patterns": [
                r"\b(crea|nuevo|inicia)\s+(un\s+)?proyecto",
                r"\btareas?\s+pendientes?\b",
                r"\bchecklist\b",
                r"\btimeline\b",
                r"\bque\s+tenemos\s+pendiente\b",
            ]
        },
        "hermes-documentos": {
            "keywords": [
                "documento", "doc", "pdf", "contrato", "carta", "reporte",
                "genera", "crea.*documento", "haz.*documento", "escribe",
                "template", "plantilla", "formato",
            ],
            "patterns": [
                r"\b(genera|crea|haz|escribe)\s+(un\s+)?(documento|contrato|carta|reporte)\b",
                r"\b(template|plantilla)\b",
            ]
        },
        "hermes-finanzas": {
            "keywords": [
                "presupuesto", "budget", "gasto", "ingreso", "costo",
                "pago", "pagado", "cobrar", "cobranza", "factura",
                "finanza", "dinero", "cuanto", "monto", "total",
                "reporte financiero", "estado de cuenta", "flujo de caja",
            ],
            "patterns": [
                r"\bpresupuesto\b",
                r"\bcuanto\s+(facturamos|ganamos|gastamos)\b",
                r"\bestado\s+de\s+cuenta\b",
            ]
        },
        "hermes-rrhh": {
            "keywords": [
                "personal", "empleado", "equipo", "staff", "nomina",
                "asistencia", "horario", "sueldo", "salario", "pago.*persona",
                "contratar", "despedir", "vacaciones",
            ],
            "patterns": [
                r"\bnomina\b",
                r"\basistencia\b",
                r"\bpersonal\b",
            ]
        },
    }
    
    def __init__(self):
        self.config = get_config()
    
    def route(self, message: str) -> Optional[str]:
        """
        Route a message to the appropriate skill.
        
        Returns skill name or None if no match.
        """
        message_lower = message.lower()
        
        scores = {}
        
        for skill_name, patterns in self.INTENT_PATTERNS.items():
            # Skip inactive departments
            dept_name = skill_name.replace("hermes-", "")
            if not self.config.departamento_activo(dept_name):
                continue
            
            score = 0
            
            # Check keywords
            for keyword in patterns["keywords"]:
                if keyword in message_lower:
                    score += 1
            
            # Check regex patterns
            for pattern in patterns["patterns"]:
                if re.search(pattern, message_lower):
                    score += 3  # Regex matches are stronger
            
            if score > 0:
                scores[skill_name] = score
        
        if not scores:
            return None
        
        # Return skill with highest score
        return max(scores, key=scores.get)
    
    def route_with_context(self, message: str, last_skill: str = None, 
                          last_client: str = None, last_project: str = None) -> Dict[str, Any]:
        """
        Route with conversation context.
        
        Returns dict with skill, client, project, and confidence.
        """
        result = {
            "skill": None,
            "client": last_client,
            "project": last_project,
            "confidence": 0.0,
        }
        
        # Try to extract client/project from message
        # Simple extraction: look for capitalized names or PROJ-XXX patterns
        client_match = re.search(r"\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b", message)
        if client_match:
            result["client"] = client_match.group(1)
        
        project_match = re.search(r"\b(PROJ-\d+)\b", message, re.IGNORECASE)
        if project_match:
            result["project"] = project_match.group(1).upper()
        
        # Route to skill
        routed_skill = self.route(message)
        
        if routed_skill:
            result["skill"] = routed_skill
            result["confidence"] = 0.8
        elif last_skill:
            # Fallback to last skill if no clear intent
            result["skill"] = last_skill
            result["confidence"] = 0.5
        
        return result


# Singleton
_router_instance = None


def get_router() -> IntentRouter:
    """Get or create singleton router instance."""
    global _router_instance
    if _router_instance is None:
        _router_instance = IntentRouter()
    return _router_instance
