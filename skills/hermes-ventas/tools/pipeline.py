"""
Hermes Business OS — Pipeline Tool
Manages sales pipeline stages, follow-ups, and alerts.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "hermes-business-core" / "tools"))

from config_loader import get_config


class Pipeline:
    """Sales pipeline manager with follow-up tracking."""
    
    PIPELINE_STAGES = [
        "lead",
        "prospecto",
        "cotizado",
        "negociacion",
        "contratado",
        "en_produccion",
        "completado",
        "entregado",
    ]
    
    # Days before triggering follow-up alert
    FOLLOW_UP_DAYS = {
        "cotizado": 3,
        "negociacion": 7,
    }
    
    def __init__(self):
        self.config = get_config()
        self.data_dir = Path(__file__).parent.parent.parent.parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.pipeline_file = self.data_dir / "pipeline.json"
        self._entries = None
        
    def _load(self) -> List[Dict[str, Any]]:
        """Load pipeline entries."""
        if self._entries is not None:
            return self._entries
        
        if self.pipeline_file.exists():
            try:
                with open(self.pipeline_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._entries = data.get("entries", [])
                    return self._entries
            except Exception:
                pass
        
        self._entries = []
        return self._entries
    
    def _save(self):
        """Save pipeline entries."""
        data = {
            "entries": self._entries,
            "updated_at": datetime.now().isoformat(),
        }
        with open(self.pipeline_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_entry(self, cliente_id: str, cliente_nombre: str,
                  proyecto_id: str = None, proyecto_nombre: str = None,
                  monto: float = 0, estado: str = "lead",
                  fuente: str = None, notas: str = None) -> Dict[str, Any]:
        """Add a new pipeline entry."""
        self._load()
        
        entry = {
            "id": f"PIPE-{len(self._entries) + 1:03d}",
            "cliente_id": cliente_id,
            "cliente_nombre": cliente_nombre,
            "proyecto_id": proyecto_id,
            "proyecto_nombre": proyecto_nombre or f"Proyecto {cliente_nombre}",
            "monto": monto,
            "estado": estado,
            "fuente": fuente or "directo",
            "fecha_entrada": datetime.now().isoformat(),
            "fecha_ultimo_cambio": datetime.now().isoformat(),
            "fecha_estimada_cierre": None,
            "notas": notas or "",
            "historial": [
                {"estado": estado, "fecha": datetime.now().isoformat(), "notas": "Registro inicial"}
            ],
        }
        
        self._entries.append(entry)
        self._save()
        
        return {
            "success": True,
            "entry": entry,
            "message": f"{cliente_nombre} agregado al pipeline como {estado}",
        }
    
    def update_stage(self, entry_id: str, nuevo_estado: str, notas: str = None) -> Dict[str, Any]:
        """Update pipeline stage for an entry."""
        self._load()
        
        if nuevo_estado not in self.PIPELINE_STAGES:
            return {
                "success": False,
                "error": f"Estado inválido. Válidos: {', '.join(self.PIPELINE_STAGES)}",
            }
        
        for entry in self._entries:
            if entry["id"].lower() == entry_id.lower():
                estado_anterior = entry["estado"]
                entry["estado"] = nuevo_estado
                entry["fecha_ultimo_cambio"] = datetime.now().isoformat()
                entry["historial"].append({
                    "estado": nuevo_estado,
                    "fecha": datetime.now().isoformat(),
                    "notas": notas or f"Cambio de {estado_anterior} a {nuevo_estado}",
                })
                self._save()
                
                return {
                    "success": True,
                    "entry": entry,
                    "message": f"{entry['cliente_nombre']}: {estado_anterior} → {nuevo_estado}",
                }
        
        return {
            "success": False,
            "error": f"Entry {entry_id} no encontrado",
        }
    
    def get_pipeline_by_stage(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get pipeline grouped by stage."""
        self._load()
        
        result = {stage: [] for stage in self.PIPELINE_STAGES}
        
        for entry in self._entries:
            stage = entry["estado"]
            if stage in result:
                result[stage].append(entry)
        
        return result
    
    def get_pipeline_summary(self) -> Dict[str, Any]:
        """Get pipeline summary with stats."""
        by_stage = self.get_pipeline_by_stage()
        moneda = self.config.moneda
        
        summary = {}
        total_value = 0
        total_count = 0
        
        for stage, entries in by_stage.items():
            stage_value = sum(e["monto"] for e in entries)
            summary[stage] = {
                "count": len(entries),
                "valor_total": stage_value,
                "entradas": entries,
            }
            total_value += stage_value
            total_count += len(entries)
        
        # Calculate conversion metrics
        leads = summary.get("lead", {}).get("count", 0) + summary.get("prospecto", {}).get("count", 0)
        contratados = summary.get("contratado", {}).get("count", 0)
        
        tasa_conversion = 0
        if leads > 0:
            tasa_conversion = (contratados / leads) * 100
        
        return {
            "total_oportunidades": total_count,
            "valor_pipeline": total_value,
            "moneda": moneda,
            "por_etapa": summary,
            "tasa_conversion": round(tasa_conversion, 1),
            "promedio_venta": round(total_value / total_count, 2) if total_count > 0 else 0,
        }
    
    def get_follow_ups(self) -> List[Dict[str, Any]]:
        """Get entries needing follow-up."""
        self._load()
        
        follow_ups = []
        now = datetime.now()
        
        for entry in self._entries:
            estado = entry["estado"]
            
            if estado not in self.FOLLOW_UP_DAYS:
                continue
            
            fecha_cambio = datetime.fromisoformat(entry["fecha_ultimo_cambio"])
            dias_transcurridos = (now - fecha_cambio).days
            dias_limite = self.FOLLOW_UP_DAYS[estado]
            
            if dias_transcurridos >= dias_limite:
                follow_ups.append({
                    "entry": entry,
                    "dias_sin_actividad": dias_transcurridos,
                    "urgencia": "alta" if dias_transcurridos > dias_limite + 3 else "media",
                    "accion_recomendada": self._recommend_action(entry, dias_transcurridos),
                })
        
        # Sort by urgency (most urgent first)
        follow_ups.sort(key=lambda x: x["dias_sin_actividad"], reverse=True)
        
        return follow_ups
    
    def _recommend_action(self, entry: Dict[str, Any], dias: int) -> str:
        """Recommend follow-up action based on stage and days."""
        estado = entry["estado"]
        
        if estado == "cotizado":
            if dias <= 5:
                return f"Enviar recordatorio amable a {entry['cliente_nombre']}"
            elif dias <= 10:
                return f"Ofrecer llamada o reunión con {entry['cliente_nombre']}"
            else:
                return f"Enviar último seguimiento o oferta especial a {entry['cliente_nombre']}"
        
        elif estado == "negociacion":
            if dias <= 10:
                return f"Revisar puntos pendientes con {entry['cliente_nombre']}"
            else:
                return f"Escalar a decisión final con {entry['cliente_nombre']}"
        
        return f"Seguimiento general con {entry['cliente_nombre']}"
    
    def format_pipeline_summary(self, summary: Dict[str, Any]) -> str:
        """Format pipeline summary for display."""
        moneda = summary["moneda"]
        lines = [
            "📊 **Pipeline de Ventas**",
            "",
            f"Total oportunidades: {summary['total_oportunidades']}",
            f"Valor total: {moneda} {summary['valor_pipeline']:,.2f}",
            f"Tasa de conversión: {summary['tasa_conversion']}%",
            f"Promedio de venta: {moneda} {summary['promedio_venta']:,.2f}",
            "",
            "**Por etapa:**",
        ]
        
        stage_emojis = {
            "lead": "👤",
            "prospecto": "🎯",
            "cotizado": "📋",
            "negociacion": "🤝",
            "contratado": "✅",
            "en_produccion": "⚙️",
            "completado": "🎉",
            "entregado": "📦",
        }
        
        for stage in self.PIPELINE_STAGES:
            data = summary["por_etapa"].get(stage, {})
            count = data.get("count", 0)
            value = data.get("valor_total", 0)
            
            if count > 0:
                emoji = stage_emojis.get(stage, "•")
                lines.append(f"{emoji} {stage.capitalize()}: {count} ({moneda} {value:,.2f})")
        
        return "\n".join(lines)
    
    def format_follow_ups(self, follow_ups: List[Dict[str, Any]]) -> str:
        """Format follow-ups for display."""
        if not follow_ups:
            return "✅ No hay seguimientos pendientes."
        
        lines = [f"🔔 **Seguimientos pendientes ({len(follow_ups)})**", ""]
        
        for fu in follow_ups:
            entry = fu["entry"]
            urgency_emoji = "🔴" if fu["urgencia"] == "alta" else "🟡"
            
            lines.append(f"{urgency_emoji} **{entry['cliente_nombre']}** — {entry['estado'].upper()}")
            lines.append(f"   Sin actividad: {fu['dias_sin_actividad']} días")
            lines.append(f"   💡 {fu['accion_recomendada']}")
            lines.append("")
        
        return "\n".join(lines)


# Singleton
_pipeline_instance = None


def get_pipeline() -> Pipeline:
    """Get or create singleton Pipeline instance."""
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = Pipeline()
    return _pipeline_instance
