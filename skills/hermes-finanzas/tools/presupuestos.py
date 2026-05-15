"""
Hermes Business OS — Presupuestos Tool
Manages project budgets with cost tracking and margin calculation.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "hermes-business-core" / "tools"))

from config_loader import get_config


class Presupuestos:
    """Budget management tool for projects."""
    
    def __init__(self):
        self.config = get_config()
        self.data_dir = Path(__file__).parent.parent.parent.parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.budgets_file = self.data_dir / "budgets.json"
        self._budgets = None
        self._next_id = 1
        
    def _load(self) -> List[Dict[str, Any]]:
        """Load budgets from JSON."""
        if self._budgets is not None:
            return self._budgets
        
        if self.budgets_file.exists():
            try:
                with open(self.budgets_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._budgets = data.get("budgets", [])
                    self._next_id = data.get("next_id", 1)
                    return self._budgets
            except Exception:
                pass
        
        self._budgets = []
        self._next_id = 1
        return self._budgets
    
    def _save(self):
        """Save budgets to JSON."""
        data = {
            "budgets": self._budgets,
            "next_id": self._next_id,
            "updated_at": datetime.now().isoformat(),
        }
        with open(self.budgets_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _generate_id(self) -> str:
        """Generate budget ID (PRE-001, PRE-002, etc.)."""
        budget_id = f"PRE-{self._next_id:03d}"
        self._next_id += 1
        return budget_id
    
    def create_budget(self, proyecto_id: str, proyecto_nombre: str,
                     ingresos: List[Dict[str, Any]],
                     costos: List[Dict[str, Any]],
                     margen_esperado: float = 30,
                     notas: str = None) -> Dict[str, Any]:
        """
        Create a new project budget.
        
        Args:
            ingresos: List of {concepto, monto} for expected income
            costos: List of {concepto, monto, tipo} for expected costs
            margen_esperado: Expected profit margin percentage
        
        Returns the created budget dict.
        """
        self._load()
        
        total_ingresos = sum(item["monto"] for item in ingresos)
        total_costos = sum(item["monto"] for item in costos)
        
        margen_bruto = total_ingresos - total_costos
        margen_porcentaje = (margen_bruto / total_ingresos * 100) if total_ingresos > 0 else 0
        
        # Categorize costs
        costos_por_tipo: Dict[str, float] = {}
        for costo in costos:
            tipo = costo.get("tipo", "otro")
            costos_por_tipo[tipo] = costos_por_tipo.get(tipo, 0) + costo["monto"]
        
        budget = {
            "id": self._generate_id(),
            "proyecto_id": proyecto_id,
            "proyecto_nombre": proyecto_nombre,
            "fecha_creacion": datetime.now().isoformat(),
            "estado": "borrador",
            "version": 1,
            "ingresos": ingresos,
            "costos": costos,
            "totales": {
                "ingresos": total_ingresos,
                "costos": total_costos,
                "margen_bruto": margen_bruto,
                "margen_porcentaje": round(margen_porcentaje, 2),
                "margen_esperado": margen_esperado,
            },
            "costos_por_tipo": costos_por_tipo,
            "notas": notas or "",
            "aprobado": False,
        }
        
        self._budgets.append(budget)
        self._save()
        
        return {
            "success": True,
            "presupuesto": budget,
            "message": f"Presupuesto {budget['id']} creado para {proyecto_nombre}",
        }
    
    def get_budget(self, budget_id: str) -> Optional[Dict[str, Any]]:
        """Get budget by ID."""
        self._load()
        for budget in self._budgets:
            if budget["id"].lower() == budget_id.lower():
                return budget
        return None
    
    def get_budget_by_project(self, proyecto_id: str) -> Optional[Dict[str, Any]]:
        """Get budget for a project."""
        self._load()
        for budget in self._budgets:
            if budget["proyecto_id"].lower() == proyecto_id.lower():
                return budget
        return None
    
    def approve_budget(self, budget_id: str) -> Dict[str, Any]:
        """Approve a budget."""
        self._load()
        
        for budget in self._budgets:
            if budget["id"].lower() == budget_id.lower():
                budget["estado"] = "aprobado"
                budget["aprobado"] = True
                budget["fecha_aprobacion"] = datetime.now().isoformat()
                self._save()
                
                return {
                    "success": True,
                    "presupuesto": budget,
                    "message": f"Presupuesto {budget_id} aprobado",
                }
        
        return {
            "success": False,
            "error": f"Presupuesto {budget_id} no encontrado",
        }
    
    def list_budgets(self, estado: str = None) -> List[Dict[str, Any]]:
        """List budgets, optionally filtered by status."""
        self._load()
        
        if estado:
            return [b for b in self._budgets if b["estado"] == estado]
        return self._budgets
    
    def get_financial_summary(self) -> Dict[str, Any]:
        """Get overall financial summary across all budgets."""
        self._load()
        
        total_ingresos = sum(b["totales"]["ingresos"] for b in self._budgets)
        total_costos = sum(b["totales"]["costos"] for b in self._budgets)
        total_margen = sum(b["totales"]["margen_bruto"] for b in self._budgets)
        
        return {
            "total_presupuestos": len(self._budgets),
            "total_ingresos": total_ingresos,
            "total_costos": total_costos,
            "total_margen": total_margen,
            "margen_promedio": round(total_margen / total_ingresos * 100, 2) if total_ingresos > 0 else 0,
            "moneda": self.config.moneda,
        }
    
    def format_budget(self, budget: Dict[str, Any]) -> str:
        """Format budget for display in conversation."""
        moneda = self.config.moneda
        t = budget["totales"]
        
        lines = [
            f"📊 **Presupuesto {budget['id']}**",
            f"Proyecto: {budget['proyecto_nombre']}",
            f"Estado: {budget['estado'].upper()}",
            "",
            "**Ingresos:**",
        ]
        
        for item in budget["ingresos"]:
            lines.append(f"  • {item['concepto']}: {moneda} {item['monto']:,.2f}")
        
        lines.extend([
            f"  Subtotal ingresos: {moneda} {t['ingresos']:,.2f}",
            "",
            "**Costos:**",
        ])
        
        for item in budget["costos"]:
            lines.append(f"  • {item['concepto']}: {moneda} {item['monto']:,.2f}")
        
        lines.extend([
            f"  Subtotal costos: {moneda} {t['costos']:,.2f}",
            "",
            f"**Margen bruto: {moneda} {t['margen_bruto']:,.2f} ({t['margen_porcentaje']}%)**",
        ])
        
        if t["margen_porcentaje"] < t["margen_esperado"]:
            lines.append(f"⚠️ Margen por debajo del esperado ({t['margen_esperado']}%)")
        
        return "\n".join(lines)


# Singleton
_presupuestos_instance = None


def get_presupuestos() -> Presupuestos:
    """Get or create singleton Presupuestos instance."""
    global _presupuestos_instance
    if _presupuestos_instance is None:
        _presupuestos_instance = Presupuestos()
    return _presupuestos_instance
