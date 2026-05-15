"""
Hermes Business OS — Reportes Financieros Tool
Generates financial reports: monthly, by project, cash flow.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "hermes-business-core" / "tools"))

from config_loader import get_config


class ReportesFinancieros:
    """Financial reporting tool."""
    
    def __init__(self):
        self.config = get_config()
        self.data_dir = Path(__file__).parent.parent.parent.parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        
    def _load_payments(self) -> List[Dict[str, Any]]:
        """Load payments data."""
        payments_file = self.data_dir / "payments.json"
        if payments_file.exists():
            try:
                with open(payments_file, "r", encoding="utf-8") as f:
                    return json.load(f).get("payments", [])
            except Exception:
                pass
        return []
    
    def _load_quotes(self) -> List[Dict[str, Any]]:
        """Load quotes data."""
        quotes_file = self.data_dir / "quotes.json"
        if quotes_file.exists():
            try:
                with open(quotes_file, "r", encoding="utf-8") as f:
                    return json.load(f).get("quotes", [])
            except Exception:
                pass
        return []
    
    def _load_budgets(self) -> List[Dict[str, Any]]:
        """Load budgets data."""
        budgets_file = self.data_dir / "budgets.json"
        if budgets_file.exists():
            try:
                with open(budgets_file, "r", encoding="utf-8") as f:
                    return json.load(f).get("budgets", [])
            except Exception:
                pass
        return []
    
    def generate_monthly_report(self, year: int = None, month: int = None) -> Dict[str, Any]:
        """Generate monthly financial report."""
        now = datetime.now()
        year = year or now.year
        month = month or now.month
        
        payments = self._load_payments()
        
        # Filter by month
        monthly_payments = []
        for p in payments:
            fecha = datetime.fromisoformat(p["fecha_creacion"])
            if fecha.year == year and fecha.month == month:
                monthly_payments.append(p)
        
        ingresos = [p for p in monthly_payments if p["tipo"] == "ingreso"]
        gastos = [p for p in monthly_payments if p["tipo"] == "gasto"]
        
        total_ingresos = sum(p["monto_total"] for p in ingresos)
        total_gastos = sum(p["monto_total"] for p in gastos)
        
        ingresos_cobrados = sum(p["monto_pagado"] for p in ingresos)
        gastos_pagados = sum(p["monto_pagado"] for p in gastos)
        
        return {
            "periodo": f"{year}-{month:02d}",
            "moneda": self.config.moneda,
            "ingresos": {
                "total": total_ingresos,
                "cobrado": ingresos_cobrados,
                "pendiente": total_ingresos - ingresos_cobrados,
                "transacciones": len(ingresos),
            },
            "gastos": {
                "total": total_gastos,
                "pagado": gastos_pagados,
                "pendiente": total_gastos - gastos_pagados,
                "transacciones": len(gastos),
            },
            "balance": ingresos_cobrados - gastos_pagados,
            "margen": round((ingresos_cobrados - gastos_pagados) / ingresos_cobrados * 100, 2) if ingresos_cobrados > 0 else 0,
        }
    
    def generate_cash_flow(self, months: int = 6) -> List[Dict[str, Any]]:
        """Generate cash flow for last N months."""
        now = datetime.now()
        cash_flow = []
        
        for i in range(months - 1, -1, -1):
            date = now - timedelta(days=i * 30)
            report = self.generate_monthly_report(date.year, date.month)
            cash_flow.append(report)
        
        return cash_flow
    
    def generate_project_report(self, proyecto_id: str) -> Dict[str, Any]:
        """Generate financial report for a specific project."""
        payments = self._load_payments()
        budgets = self._load_budgets()
        quotes = self._load_quotes()
        
        project_payments = [p for p in payments if p["proyecto_id"].lower() == proyecto_id.lower()]
        project_budgets = [b for b in budgets if b["proyecto_id"].lower() == proyecto_id.lower()]
        project_quotes = [q for q in quotes if q.get("proyecto_id", "").lower() == proyecto_id.lower()]
        
        ingresos = [p for p in project_payments if p["tipo"] == "ingreso"]
        gastos = [p for p in project_payments if p["tipo"] == "gasto"]
        
        total_ingresos = sum(p["monto_total"] for p in ingresos)
        total_gastos = sum(p["monto_total"] for p in gastos)
        
        return {
            "proyecto_id": proyecto_id,
            "moneda": self.config.moneda,
            "presupuestos": project_budgets,
            "cotizaciones": project_quotes,
            "ingresos": {
                "total": total_ingresos,
                "cobrado": sum(p["monto_pagado"] for p in ingresos),
                "pendiente": sum(p["monto_pendiente"] for p in ingresos),
            },
            "gastos": {
                "total": total_gastos,
                "pagado": sum(p["monto_pagado"] for p in gastos),
                "pendiente": sum(p["monto_pendiente"] for p in gastos),
            },
            "balance": total_ingresos - total_gastos,
        }
    
    def get_accounts_receivable(self) -> List[Dict[str, Any]]:
        """Get all accounts receivable (pending income)."""
        payments = self._load_payments()
        return [p for p in payments if p["tipo"] == "ingreso" and p["estado"] in ["pendiente", "parcial"]]
    
    def get_accounts_payable(self) -> List[Dict[str, Any]]:
        """Get all accounts payable (pending expenses)."""
        payments = self._load_payments()
        return [p for p in payments if p["tipo"] == "gasto" and p["estado"] in ["pendiente", "parcial"]]
    
    def format_monthly_report(self, report: Dict[str, Any]) -> str:
        """Format monthly report for display."""
        moneda = report["moneda"]
        lines = [
            f"📊 **Reporte Financiero — {report['periodo']}**",
            "",
            f"**Ingresos:**",
            f"  Total: {moneda} {report['ingresos']['total']:,.2f}",
            f"  Cobrado: {moneda} {report['ingresos']['cobrado']:,.2f}",
            f"  Pendiente: {moneda} {report['ingresos']['pendiente']:,.2f}",
            f"  Transacciones: {report['ingresos']['transacciones']}",
            "",
            f"**Gastos:**",
            f"  Total: {moneda} {report['gastos']['total']:,.2f}",
            f"  Pagado: {moneda} {report['gastos']['pagado']:,.2f}",
            f"  Pendiente: {moneda} {report['gastos']['pendiente']:,.2f}",
            f"  Transacciones: {report['gastos']['transacciones']}",
            "",
            f"**Balance: {moneda} {report['balance']:,.2f}**",
            f"**Margen: {report['margen']}%**",
        ]
        return "\n".join(lines)
    
    def format_cash_flow(self, cash_flow: List[Dict[str, Any]]) -> str:
        """Format cash flow report."""
        if not cash_flow:
            return "No hay datos de flujo de caja."
        
        moneda = cash_flow[0]["moneda"]
        lines = ["💰 **Flujo de Caja**\n"]
        
        for report in cash_flow:
            balance_emoji = "🟢" if report["balance"] >= 0 else "🔴"
            lines.append(f"{balance_emoji} **{report['periodo']}**")
            lines.append(f"   Ingresos: {moneda} {report['ingresos']['cobrado']:,.2f}")
            lines.append(f"   Gastos: {moneda} {report['gastos']['pagado']:,.2f}")
            lines.append(f"   Balance: {moneda} {report['balance']:,.2f}")
            lines.append("")
        
        return "\n".join(lines)


# Singleton
_reportes_instance = None


def get_reportes() -> ReportesFinancieros:
    """Get or create singleton ReportesFinancieros instance."""
    global _reportes_instance
    if _reportes_instance is None:
        _reportes_instance = ReportesFinancieros()
    return _reportes_instance
