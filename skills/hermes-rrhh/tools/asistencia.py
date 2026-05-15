"""
Hermes Business OS — Asistencia Tool
Tracks attendance, hours worked, and payroll calculation.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "hermes-business-core" / "tools"))

from config_loader import get_config


class Asistencia:
    """Attendance and payroll tracking tool."""
    
    def __init__(self):
        self.config = get_config()
        self.data_dir = Path(__file__).parent.parent.parent.parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.attendance_file = self.data_dir / "attendance.json"
        self._records = None
        
    def _load(self) -> List[Dict[str, Any]]:
        """Load attendance records from JSON."""
        if self._records is not None:
            return self._records
        
        if self.attendance_file.exists():
            try:
                with open(self.attendance_file, "r", encoding="utf-8") as f:
                    self._records = json.load(f).get("records", [])
                    return self._records
            except Exception:
                pass
        
        self._records = []
        return self._records
    
    def _save(self):
        """Save attendance records to JSON."""
        data = {
            "records": self._records,
            "updated_at": datetime.now().isoformat(),
        }
        with open(self.attendance_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def register_entry(self, member_id: str, member_nombre: str,
                      proyecto_id: str = None, proyecto_nombre: str = None,
                      fecha: str = None, horas: float = 8,
                      tipo: str = "trabajo",  # trabajo | descanso | vacaciones | incapacidad
                      notas: str = None) -> Dict[str, Any]:
        """
        Register an attendance entry.
        
        Returns the created record dict.
        """
        self._load()
        
        if fecha and isinstance(fecha, str):
            try:
                fecha_dt = datetime.fromisoformat(fecha.replace("Z", "+00:00"))
            except ValueError:
                fecha_dt = datetime.now()
        else:
            fecha_dt = datetime.now()
        
        record = {
            "id": f"ASIS-{len(self._records) + 1:04d}",
            "member_id": member_id,
            "member_nombre": member_nombre,
            "proyecto_id": proyecto_id,
            "proyecto_nombre": proyecto_nombre,
            "fecha": fecha_dt.strftime("%Y-%m-%d"),
            "hora_entrada": fecha_dt.strftime("%H:%M"),
            "horas": horas,
            "tipo": tipo,
            "notas": notas or "",
            "registrado_en": datetime.now().isoformat(),
        }
        
        self._records.append(record)
        self._save()
        
        return {
            "success": True,
            "registro": record,
            "message": f"Asistencia registrada: {member_nombre} — {horas}h ({fecha_dt.strftime('%Y-%m-%d')})",
        }
    
    def get_attendance_by_member(self, member_id: str,
                                 fecha_inicio: str = None,
                                 fecha_fin: str = None) -> List[Dict[str, Any]]:
        """Get attendance records for a member in a date range."""
        self._load()
        
        records = [r for r in self._records if r["member_id"].lower() == member_id.lower()]
        
        if fecha_inicio:
            records = [r for r in records if r["fecha"] >= fecha_inicio]
        if fecha_fin:
            records = [r for r in records if r["fecha"] <= fecha_fin]
        
        return sorted(records, key=lambda r: r["fecha"])
    
    def get_attendance_by_project(self, proyecto_id: str,
                                  fecha_inicio: str = None,
                                  fecha_fin: str = None) -> List[Dict[str, Any]]:
        """Get attendance records for a project in a date range."""
        self._load()
        
        records = [r for r in self._records if r.get("proyecto_id") == proyecto_id]
        
        if fecha_inicio:
            records = [r for r in records if r["fecha"] >= fecha_inicio]
        if fecha_fin:
            records = [r for r in records if r["fecha"] <= fecha_fin]
        
        return sorted(records, key=lambda r: r["fecha"])
    
    def calculate_payroll(self, member_id: str, member_nombre: str,
                         tarifa_dia: float, tarifa_hora: float = None,
                         fecha_inicio: str = None, fecha_fin: str = None) -> Dict[str, Any]:
        """
        Calculate payroll for a member in a date range.
        
        Returns payroll breakdown.
        """
        records = self.get_attendance_by_member(member_id, fecha_inicio, fecha_fin)
        
        total_horas = sum(r["horas"] for r in records if r["tipo"] == "trabajo")
        dias_trabajados = len([r for r in records if r["tipo"] == "trabajo"])
        dias_descanso = len([r for r in records if r["tipo"] == "descanso"])
        dias_vacaciones = len([r for r in records if r["tipo"] == "vacaciones"])
        
        # Calculate pay
        if tarifa_hora:
            pago = total_horas * tarifa_hora
        else:
            pago = dias_trabajados * tarifa_dia
        
        moneda = self.config.moneda
        
        return {
            "member_id": member_id,
            "member_nombre": member_nombre,
            "periodo": {
                "inicio": fecha_inicio or records[0]["fecha"] if records else None,
                "fin": fecha_fin or records[-1]["fecha"] if records else None,
            },
            "moneda": moneda,
            "resumen": {
                "dias_trabajados": dias_trabajados,
                "dias_descanso": dias_descanso,
                "dias_vacaciones": dias_vacaciones,
                "total_horas": total_horas,
            },
            "pago": {
                "tarifa_dia": tarifa_dia,
                "tarifa_hora": tarifa_hora,
                "subtotal": pago,
            },
            "registros": records,
        }
    
    def get_attendance_summary(self, fecha_inicio: str = None, fecha_fin: str = None) -> Dict[str, Any]:
        """Get overall attendance summary."""
        self._load()
        
        records = self._records
        
        if fecha_inicio:
            records = [r for r in records if r["fecha"] >= fecha_inicio]
        if fecha_fin:
            records = [r for r in records if r["fecha"] <= fecha_fin]
        
        total_registros = len(records)
        horas_trabajadas = sum(r["horas"] for r in records if r["tipo"] == "trabajo")
        
        # By member
        by_member: Dict[str, Dict[str, Any]] = {}
        for r in records:
            mid = r["member_id"]
            if mid not in by_member:
                by_member[mid] = {"nombre": r["member_nombre"], "horas": 0, "dias": 0}
            by_member[mid]["horas"] += r["horas"]
            by_member[mid]["dias"] += 1
        
        return {
            "total_registros": total_registros,
            "horas_trabajadas": horas_trabajadas,
            "by_member": by_member,
        }
    
    def format_payroll(self, payroll: Dict[str, Any]) -> str:
        """Format payroll for display."""
        moneda = payroll["moneda"]
        r = payroll["resumen"]
        p = payroll["pago"]
        
        lines = [
            f"💰 **Nómina — {payroll['member_nombre']}**",
            f"",
            f"**Periodo:** {payroll['periodo']['inicio']} a {payroll['periodo']['fin']}",
            f"",
            f"**Resumen:**",
            f"  Días trabajados: {r['dias_trabajados']}",
            f"  Días de descanso: {r['dias_descanso']}",
            f"  Días de vacaciones: {r['dias_vacaciones']}",
            f"  Total horas: {r['total_horas']}",
            f"",
            f"**Pago:**",
            f"  Tarifa/día: {moneda} {p['tarifa_dia']:,.2f}",
        ]
        
        if p["tarifa_hora"]:
            lines.append(f"  Tarifa/hora: {moneda} {p['tarifa_hora']:,.2f}")
        
        lines.append(f"  **Total a pagar: {moneda} {p['subtotal']:,.2f}**")
        
        return "\n".join(lines)


# Singleton
_asistencia_instance = None


def get_asistencia() -> Asistencia:
    """Get or create singleton Asistencia instance."""
    global _asistencia_instance
    if _asistencia_instance is None:
        _asistencia_instance = Asistencia()
    return _asistencia_instance
