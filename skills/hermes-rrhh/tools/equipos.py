"""
Hermes Business OS — Equipos Tool
Manages team members, roles, and assignments.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "hermes-business-core" / "tools"))

from config_loader import get_config


class Equipos:
    """Team management tool."""
    
    def __init__(self):
        self.config = get_config()
        self.data_dir = Path(__file__).parent.parent.parent.parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.team_file = self.data_dir / "team.json"
        self._members = None
        self._next_id = 1
        
    def _load(self) -> List[Dict[str, Any]]:
        """Load team members from JSON."""
        if self._members is not None:
            return self._members
        
        if self.team_file.exists():
            try:
                with open(self.team_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._members = data.get("members", [])
                    self._next_id = data.get("next_id", 1)
                    return self._members
            except Exception:
                pass
        
        self._members = []
        self._next_id = 1
        return self._members
    
    def _save(self):
        """Save team members to JSON."""
        data = {
            "members": self._members,
            "next_id": self._next_id,
            "updated_at": datetime.now().isoformat(),
        }
        with open(self.team_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _generate_id(self) -> str:
        """Generate member ID (EMP-001, EMP-002, etc.)."""
        member_id = f"EMP-{self._next_id:03d}"
        self._next_id += 1
        return member_id
    
    def add_member(self, nombre: str, rol: str = None,
                  email: str = None, telefono: str = None,
                  tarifa_dia: float = 0, tarifa_hora: float = 0,
                  skills: List[str] = None, notas: str = None) -> Dict[str, Any]:
        """
        Add a new team member.
        
        Returns the created member dict.
        """
        self._load()
        
        member = {
            "id": self._generate_id(),
            "nombre": nombre,
            "rol": rol or "General",
            "email": email,
            "telefono": telefono,
            "tarifa_dia": tarifa_dia,
            "tarifa_hora": tarifa_hora,
            "skills": skills or [],
            "estado": "activo",
            "fecha_registro": datetime.now().isoformat(),
            "proyectos_asignados": [],
            "notas": notas or "",
        }
        
        self._members.append(member)
        self._save()
        
        return {
            "success": True,
            "miembro": member,
            "message": f"Miembro agregado: {nombre} ({member['id']})",
        }
    
    def get_member(self, member_id: str) -> Optional[Dict[str, Any]]:
        """Get member by ID."""
        self._load()
        for member in self._members:
            if member["id"].lower() == member_id.lower():
                return member
        return None
    
    def find_member(self, query: str) -> Optional[Dict[str, Any]]:
        """Find member by name or ID."""
        self._load()
        query_lower = query.lower()
        
        for member in self._members:
            if member["id"].lower() == query_lower:
                return member
            if query_lower in member["nombre"].lower():
                return member
        return None
    
    def update_member(self, member_id: str, **updates) -> Dict[str, Any]:
        """Update member fields."""
        self._load()
        
        for member in self._members:
            if member["id"].lower() == member_id.lower():
                safe_updates = {k: v for k, v in updates.items() if k not in ["id", "fecha_registro"]}
                member.update(safe_updates)
                self._save()
                
                return {
                    "success": True,
                    "miembro": member,
                    "message": f"Miembro {member_id} actualizado",
                }
        
        return {
            "success": False,
            "error": f"Miembro {member_id} no encontrado",
        }
    
    def assign_to_project(self, member_id: str, proyecto_id: str,
                         proyecto_nombre: str = None) -> Dict[str, Any]:
        """Assign a member to a project."""
        self._load()
        
        for member in self._members:
            if member["id"].lower() == member_id.lower():
                if proyecto_id not in member["proyectos_asignados"]:
                    member["proyectos_asignados"].append(proyecto_id)
                    self._save()
                
                return {
                    "success": True,
                    "message": f"{member['nombre']} asignado a {proyecto_id}",
                }
        
        return {
            "success": False,
            "error": f"Miembro {member_id} no encontrado",
        }
    
    def list_members(self, rol: str = None, estado: str = None) -> List[Dict[str, Any]]:
        """List team members, optionally filtered."""
        self._load()
        
        members = self._members
        
        if rol:
            members = [m for m in members if m["rol"] == rol]
        if estado:
            members = [m for m in members if m["estado"] == estado]
        
        return members
    
    def get_members_by_project(self, proyecto_id: str) -> List[Dict[str, Any]]:
        """Get members assigned to a project."""
        self._load()
        return [m for m in self._members if proyecto_id in m.get("proyectos_asignados", [])]
    
    def get_team_summary(self) -> Dict[str, Any]:
        """Get team summary."""
        self._load()
        
        total = len(self._members)
        activos = len([m for m in self._members if m["estado"] == "activo"])
        inactivos = len([m for m in self._members if m["estado"] == "inactivo"])
        
        roles: Dict[str, int] = {}
        for m in self._members:
            roles[m["rol"]] = roles.get(m["rol"], 0) + 1
        
        return {
            "total": total,
            "activos": activos,
            "inactivos": inactivos,
            "roles": roles,
            "members": self._members,
        }
    
    def format_member(self, member: Dict[str, Any]) -> str:
        """Format member for display."""
        lines = [
            f"👤 **{member['nombre']}** ({member['id']})",
            f"Rol: {member['rol']}",
            f"Estado: {member['estado']}",
        ]
        
        if member.get("email"):
            lines.append(f"Email: {member['email']}")
        if member.get("telefono"):
            lines.append(f"Teléfono: {member['telefono']}")
        if member.get("tarifa_dia"):
            lines.append(f"Tarifa/día: {self.config.moneda} {member['tarifa_dia']:,.2f}")
        if member.get("skills"):
            lines.append(f"Skills: {', '.join(member['skills'])}")
        if member.get("proyectos_asignados"):
            lines.append(f"Proyectos: {', '.join(member['proyectos_asignados'])}")
        
        return "\n".join(lines)


# Singleton
_equipos_instance = None


def get_equipos() -> Equipos:
    """Get or create singleton Equipos instance."""
    global _equipos_instance
    if _equipos_instance is None:
        _equipos_instance = Equipos()
    return _equipos_instance
