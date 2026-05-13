"""
Skill: Operaciones - Operations department
Projects, tasks, timelines, logistics
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from app.skills.base import BaseSkill, action


class OperacionesSkill(BaseSkill):
    """Operations skill for project management and task tracking."""
    
    name = "operaciones"
    description = "Proyectos, tareas, timelines y logistica operativa"
    version = "1.0.0"
    
    def _register_actions(self) -> Dict[str, callable]:
        return {
            "crear_proyecto": self.crear_proyecto,
            "listar_proyectos": self.listar_proyectos,
            "crear_tarea": self.crear_tarea,
            "asignar_tarea": self.asignar_tarea,
            "generar_timeline": self.generar_timeline,
            "checklist_proyecto": self.checklist_proyecto,
        }
    
    @action("Crear un nuevo proyecto")
    def crear_proyecto(self, nombre: str, cliente: str = None, 
                       descripcion: str = None, fecha_inicio: str = None,
                       fecha_fin: str = None, presupuesto: float = 0) -> Dict[str, Any]:
        """Create a new project."""
        inicio = fecha_inicio or datetime.now().strftime("%Y-%m-%d")
        
        return {
            "proyecto": {
                "nombre": nombre,
                "cliente": cliente,
                "descripcion": descripcion,
                "fecha_inicio": inicio,
                "fecha_fin": fecha_fin,
                "presupuesto": presupuesto,
                "estado": "planificacion",
                "progreso": 0
            },
            "mensaje": f"Proyecto '{nombre}' creado exitosamente",
            "siguiente_paso": "Agregar tareas y asignar recursos"
        }
    
    @action("Listar proyectos activos")
    def listar_proyectos(self, estado: str = None, limite: int = 20) -> Dict[str, Any]:
        """List projects with filtering."""
        return {
            "filtro": estado or "todos",
            "proyectos": [],  # Would query DB
            "mensaje": "Usa el dashboard para ver proyectos completos"
        }
    
    @action("Crear tarea dentro de un proyecto")
    def crear_tarea(self, proyecto: str, nombre: str, descripcion: str = None,
                    asignado_a: str = None, fecha_limite: str = None,
                    prioridad: str = "media") -> Dict[str, Any]:
        """Create a task within a project."""
        return {
            "tarea": {
                "proyecto": proyecto,
                "nombre": nombre,
                "descripcion": descripcion,
                "asignado_a": asignado_a,
                "fecha_limite": fecha_limite,
                "prioridad": prioridad,
                "estado": "pendiente"
            },
            "mensaje": f"Tarea '{nombre}' creada en proyecto '{proyecto}'",
            "siguiente_paso": "Asignar a responsable si no está asignada"
        }
    
    @action("Asignar tarea a un miembro del equipo")
    def asignar_tarea(self, tarea_id: str, usuario: str) -> Dict[str, Any]:
        """Assign a task to a team member."""
        return {
            "asignacion": {
                "tarea": tarea_id,
                "asignado_a": usuario,
                "fecha_asignacion": datetime.now().isoformat()
            },
            "mensaje": f"Tarea asignada a {usuario}",
            "notificacion": f"Se notificará a {usuario} por Telegram"
        }
    
    @action("Generar timeline de proyecto")
    def generar_timeline(self, proyecto: str, tareas: List[Dict] = None) -> Dict[str, Any]:
        """Generate project timeline."""
        # Simple timeline generation
        timeline = []
        if tareas:
            for i, tarea in enumerate(tareas):
                dias = tarea.get("duracion_dias", 1)
                inicio = datetime.now() + timedelta(days=i * 2)
                fin = inicio + timedelta(days=dias)
                timeline.append({
                    "tarea": tarea.get("nombre"),
                    "inicio": inicio.strftime("%Y-%m-%d"),
                    "fin": fin.strftime("%Y-%m-%d"),
                    "duracion": dias
                })
        
        return {
            "proyecto": proyecto,
            "timeline": timeline,
            "formato": "gantt_simple",
            "mensaje": f"Timeline generado con {len(timeline)} tareas"
        }
    
    @action("Generar checklist de proyecto")
    def checklist_proyecto(self, tipo: str = "general") -> Dict[str, Any]:
        """Generate project checklist by type."""
        checklists = {
            "general": [
                "Definir alcance y objetivos",
                "Asignar responsables",
                "Establecer fechas clave",
                "Revisar presupuesto",
                "Comunicar al cliente"
            ],
            "evento": [
                "Confirmar fecha y lugar",
                "Revisar inventario necesario",
                "Coordinar proveedores",
                "Confirmar staff",
                "Preparar materiales",
                "Montaje previo",
                "Día del evento",
                "Desmontaje y registro"
            ],
            "legal": [
                "Recibir documentación",
                "Analizar jurisprudencia",
                "Redactar escrito",
                "Revisión interna",
                "Aprobación del cliente",
                "Presentar en juzgado",
                "Seguimiento"
            ]
        }
        
        items = checklists.get(tipo, checklists["general"])
        return {
            "tipo": tipo,
            "checklist": [{"item": item, "completado": False} for item in items],
            "total": len(items),
            "mensaje": f"Checklist de {tipo} generado con {len(items)} items"
        }
