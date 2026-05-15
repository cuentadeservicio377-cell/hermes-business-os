"""
Hermes Business OS — CRM Tool
Manages clients, prospects, and contacts.
Uses Google Sheets as master database or local JSON fallback.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "hermes-business-core" / "tools"))

from config_loader import get_config


try:
    from google_workspace import get_google_workspace
    GW_AVAILABLE = True
except ImportError:
    GW_AVAILABLE = False


class CRM:
    """Customer Relationship Management tool."""
    
    def __init__(self):
        self.config = get_config()
        self.data_dir = Path(__file__).parent.parent.parent.parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.clients_file = self.data_dir / "clients.json"
        self._clients = None
        self._next_id = 1
        
    def _load_clients(self) -> List[Dict[str, Any]]:
        """Load clients from local JSON or Google Sheets."""
        if self._clients is not None:
            return self._clients
        
        # Try local JSON first
        if self.clients_file.exists():
            try:
                with open(self.clients_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._clients = data.get("clients", [])
                    self._next_id = data.get("next_id", 1)
                    return self._clients
            except Exception:
                pass
        
        # Try Google Sheets
        if GW_AVAILABLE and self.config.integracion_activa("google_workspace"):
            try:
                gw = get_google_workspace()
                # Try to find master spreadsheet
                # This is a simplified version; real implementation would search Drive
                pass
            except Exception:
                pass
        
        self._clients = []
        self._next_id = 1
        return self._clients
    
    def _save_clients(self):
        """Save clients to local JSON."""
        data = {
            "clients": self._clients,
            "next_id": self._next_id,
            "updated_at": datetime.now().isoformat(),
        }
        with open(self.clients_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _generate_client_id(self) -> str:
        """Generate next client ID (CLI-001, CLI-002, etc.)."""
        client_id = f"CLI-{self._next_id:03d}"
        self._next_id += 1
        return client_id
    
    def add_client(self, nombre: str, email: str = None, telefono: str = None,
                   tipo_proyecto: str = None, fuente: str = None,
                   notas: str = None, **kwargs) -> Dict[str, Any]:
        """
        Add a new client/prospect.
        
        Returns the created client dict.
        """
        self._load_clients()
        
        # Check if client already exists
        existing = self.find_client(nombre)
        if existing:
            return {
                "success": False,
                "error": f"Cliente '{nombre}' ya existe (ID: {existing['id']})",
                "cliente": existing,
            }
        
        client = {
            "id": self._generate_client_id(),
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "tipo_proyecto": tipo_proyecto,
            "fuente": fuente or "directo",
            "estado": "lead",
            "notas": notas or "",
            "fecha_registro": datetime.now().isoformat(),
            "ultima_actualizacion": datetime.now().isoformat(),
            "proyectos": [],
        }
        
        # Add any extra fields
        client.update(kwargs)
        
        self._clients.append(client)
        self._save_clients()
        
        return {
            "success": True,
            "cliente": client,
            "message": f"Cliente registrado: {nombre} ({client['id']})",
        }
    
    def find_client(self, query: str) -> Optional[Dict[str, Any]]:
        """Find client by name, ID, or partial match."""
        self._load_clients()
        
        query_lower = query.lower()
        
        for client in self._clients:
            # Exact ID match
            if client["id"].lower() == query_lower:
                return client
            # Name contains query
            if query_lower in client["nombre"].lower():
                return client
            # Email match
            if client.get("email") and query_lower in client["email"].lower():
                return client
        
        return None
    
    def get_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get client by exact ID."""
        self._load_clients()
        
        for client in self._clients:
            if client["id"].lower() == client_id.lower():
                return client
        
        return None
    
    def update_client(self, client_id: str, **updates) -> Dict[str, Any]:
        """Update client fields."""
        self._load_clients()
        
        for client in self._clients:
            if client["id"].lower() == client_id.lower():
                client.update(updates)
                client["ultima_actualizacion"] = datetime.now().isoformat()
                self._save_clients()
                
                return {
                    "success": True,
                    "cliente": client,
                    "message": f"Cliente {client_id} actualizado",
                }
        
        return {
            "success": False,
            "error": f"Cliente {client_id} no encontrado",
        }
    
    def update_status(self, client_id: str, nuevo_estado: str) -> Dict[str, Any]:
        """Update client status (lead → prospecto → cotizado → contratado, etc.)."""
        estados_validos = ["lead", "prospecto", "cotizado", "negociacion", "contratado", 
                          "en_produccion", "completado", "entregado", "perdido", "descartado"]
        
        if nuevo_estado not in estados_validos:
            return {
                "success": False,
                "error": f"Estado inválido. Válidos: {', '.join(estados_validos)}",
            }
        
        return self.update_client(client_id, estado=nuevo_estado)
    
    def list_clients(self, estado: str = None) -> List[Dict[str, Any]]:
        """List all clients, optionally filtered by status."""
        self._load_clients()
        
        if estado:
            return [c for c in self._clients if c["estado"] == estado]
        
        return self._clients
    
    def add_project_to_client(self, client_id: str, project_id: str) -> Dict[str, Any]:
        """Link a project to a client."""
        self._load_clients()
        
        for client in self._clients:
            if client["id"].lower() == client_id.lower():
                if project_id not in client["proyectos"]:
                    client["proyectos"].append(project_id)
                    self._save_clients()
                
                return {
                    "success": True,
                    "message": f"Proyecto {project_id} vinculado a {client_id}",
                }
        
        return {
            "success": False,
            "error": f"Cliente {client_id} no encontrado",
        }
    
    def get_pipeline_summary(self) -> Dict[str, Any]:
        """Get pipeline summary with counts and values per stage."""
        self._load_clients()
        
        pipeline = {}
        for estado in ["lead", "prospecto", "cotizado", "negociacion", "contratado"]:
            clients = [c for c in self._clients if c["estado"] == estado]
            pipeline[estado] = {
                "count": len(clients),
                "clientes": clients,
            }
        
        total = len(self._clients)
        
        return {
            "total_clientes": total,
            "pipeline": pipeline,
            "por_convertir": len([c for c in self._clients if c["estado"] in ["lead", "prospecto", "cotizado", "negociacion"]]),
            "activos": len([c for c in self._clients if c["estado"] in ["contratado", "en_produccion"]]),
        }
    
    def extract_client_from_message(self, message: str) -> Optional[str]:
        """Try to extract a client name from a natural language message."""
        # Look for capitalized names (simple heuristic)
        patterns = [
            r"(?:cliente|para|de)\s+([A-Z][a-z]+\s+(?:[A-Z][a-z]+\s*)+)",
            r"([A-Z][a-z]+\s+[A-Z][a-z]+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                name = match.group(1).strip()
                # Verify it's a real client
                client = self.find_client(name)
                if client:
                    return client["nombre"]
        
        return None


# Singleton
_crm_instance = None


def get_crm() -> CRM:
    """Get or create singleton CRM instance."""
    global _crm_instance
    if _crm_instance is None:
        _crm_instance = CRM()
    return _crm_instance
