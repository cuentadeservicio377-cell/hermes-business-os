"""
Hermes Business OS — Pagos Tool
Manages payments, invoices, and collection tracking.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "hermes-business-core" / "tools"))

from config_loader import get_config


class Pagos:
    """Payment tracking and invoice management."""
    
    PAYMENT_STATUSES = [
        "pendiente",
        "parcial",
        "pagado",
        "facturado",
        "vencido",
        "cobranza",
        "incobrable",
    ]
    
    def __init__(self):
        self.config = get_config()
        self.data_dir = Path(__file__).parent.parent.parent.parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        self.payments_file = self.data_dir / "payments.json"
        self._payments = None
        self._next_id = 1
        
    def _load(self) -> List[Dict[str, Any]]:
        """Load payments from JSON."""
        if self._payments is not None:
            return self._payments
        
        if self.payments_file.exists():
            try:
                with open(self.payments_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._payments = data.get("payments", [])
                    self._next_id = data.get("next_id", 1)
                    return self._payments
            except Exception:
                pass
        
        self._payments = []
        self._next_id = 1
        return self._payments
    
    def _save(self):
        """Save payments to JSON."""
        data = {
            "payments": self._payments,
            "next_id": self._next_id,
            "updated_at": datetime.now().isoformat(),
        }
        with open(self.payments_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _generate_id(self) -> str:
        """Generate payment ID (PAG-001, PAG-002, etc.)."""
        payment_id = f"PAG-{self._next_id:03d}"
        self._next_id += 1
        return payment_id
    
    def register_payment(self, proyecto_id: str, proyecto_nombre: str,
                        cliente_id: str, cliente_nombre: str,
                        monto_total: float, concepto: str,
                        tipo: str = "ingreso",  # ingreso | gasto
                        fecha_vencimiento: str = None,
                        metodo_pago: str = None) -> Dict[str, Any]:
        """
        Register a new payment/invoice.
        
        Returns the created payment dict.
        """
        self._load()
        
        if fecha_vencimiento and isinstance(fecha_vencimiento, str):
            try:
                fecha_vencimiento_dt = datetime.fromisoformat(fecha_vencimiento.replace("Z", "+00:00"))
            except ValueError:
                fecha_vencimiento_dt = datetime.now() + timedelta(days=30)
        else:
            fecha_vencimiento_dt = datetime.now() + timedelta(days=30)
        
        payment = {
            "id": self._generate_id(),
            "proyecto_id": proyecto_id,
            "proyecto_nombre": proyecto_nombre,
            "cliente_id": cliente_id,
            "cliente_nombre": cliente_nombre,
            "concepto": concepto,
            "tipo": tipo,  # ingreso | gasto
            "monto_total": monto_total,
            "monto_pagado": 0,
            "monto_pendiente": monto_total,
            "estado": "pendiente",
            "fecha_creacion": datetime.now().isoformat(),
            "fecha_vencimiento": fecha_vencimiento_dt.isoformat(),
            "fecha_pago": None,
            "metodo_pago": metodo_pago,
            "transacciones": [],
        }
        
        self._payments.append(payment)
        self._save()
        
        return {
            "success": True,
            "pago": payment,
            "message": f"Pago {payment['id']} registrado: {concepto} ({self.config.moneda} {monto_total:,.2f})",
        }
    
    def add_transaction(self, payment_id: str, monto: float,
                       metodo: str = None, notas: str = None) -> Dict[str, Any]:
        """Add a partial or full payment transaction."""
        self._load()
        
        for payment in self._payments:
            if payment["id"].lower() == payment_id.lower():
                transaction = {
                    "monto": monto,
                    "fecha": datetime.now().isoformat(),
                    "metodo": metodo or "no especificado",
                    "notas": notas or "",
                }
                payment["transacciones"].append(transaction)
                payment["monto_pagado"] += monto
                payment["monto_pendiente"] = payment["monto_total"] - payment["monto_pagado"]
                
                # Update status
                if payment["monto_pagado"] >= payment["monto_total"]:
                    payment["estado"] = "pagado"
                    payment["fecha_pago"] = datetime.now().isoformat()
                elif payment["monto_pagado"] > 0:
                    payment["estado"] = "parcial"
                
                self._save()
                
                return {
                    "success": True,
                    "pago": payment,
                    "message": f"Transacción registrada: {self.config.moneda} {monto:,.2f}. Pendiente: {self.config.moneda} {payment['monto_pendiente']:,.2f}",
                }
        
        return {
            "success": False,
            "error": f"Pago {payment_id} no encontrado",
        }
    
    def get_payment(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """Get payment by ID."""
        self._load()
        for payment in self._payments:
            if payment["id"].lower() == payment_id.lower():
                return payment
        return None
    
    def update_status(self, payment_id: str, nuevo_estado: str) -> Dict[str, Any]:
        """Update payment status."""
        if nuevo_estado not in self.PAYMENT_STATUSES:
            return {
                "success": False,
                "error": f"Estado inválido. Válidos: {', '.join(self.PAYMENT_STATUSES)}",
            }
        
        self._load()
        
        for payment in self._payments:
            if payment["id"].lower() == payment_id.lower():
                payment["estado"] = nuevo_estado
                self._save()
                
                return {
                    "success": True,
                    "pago": payment,
                    "message": f"Pago {payment_id}: estado → {nuevo_estado}",
                }
        
        return {
            "success": False,
            "error": f"Pago {payment_id} no encontrado",
        }
    
    def get_overdue_payments(self) -> List[Dict[str, Any]]:
        """Get overdue payments (both income and expenses)."""
        self._load()
        now = datetime.now()
        
        overdue = []
        for payment in self._payments:
            if payment["estado"] in ["pendiente", "parcial"]:
                fecha_vencimiento = datetime.fromisoformat(payment["fecha_vencimiento"])
                if fecha_vencimiento < now:
                    dias_vencido = (now - fecha_vencimiento).days
                    payment["_dias_vencido"] = dias_vencido
                    overdue.append(payment)
        
        overdue.sort(key=lambda p: p["_dias_vencido"], reverse=True)
        return overdue
    
    def get_payment_summary(self) -> Dict[str, Any]:
        """Get payment summary."""
        self._load()
        
        ingresos = [p for p in self._payments if p["tipo"] == "ingreso"]
        gastos = [p for p in self._payments if p["tipo"] == "gasto"]
        
        total_ingresos = sum(p["monto_total"] for p in ingresos)
        total_gastos = sum(p["monto_total"] for p in gastos)
        
        ingresos_cobrados = sum(p["monto_pagado"] for p in ingresos)
        gastos_pagados = sum(p["monto_pagado"] for p in gastos)
        
        por_cobrar = sum(p["monto_pendiente"] for p in ingresos if p["estado"] in ["pendiente", "parcial"])
        por_pagar = sum(p["monto_pendiente"] for p in gastos if p["estado"] in ["pendiente", "parcial"])
        
        return {
            "moneda": self.config.moneda,
            "total_transacciones": len(self._payments),
            "ingresos": {
                "total": total_ingresos,
                "cobrado": ingresos_cobrados,
                "por_cobrar": por_cobrar,
            },
            "gastos": {
                "total": total_gastos,
                "pagado": gastos_pagados,
                "por_pagar": por_pagar,
            },
            "balance": ingresos_cobrados - gastos_pagados,
            "vencidos": len(self.get_overdue_payments()),
        }
    
    def format_payment(self, payment: Dict[str, Any]) -> str:
        """Format payment for display."""
        moneda = self.config.moneda
        
        lines = [
            f"💰 **{payment['id']}** — {payment['concepto']}",
            f"Cliente: {payment['cliente_nombre']}",
            f"Proyecto: {payment['proyecto_nombre']}",
            f"",
            f"Total: {moneda} {payment['monto_total']:,.2f}",
            f"Pagado: {moneda} {payment['monto_pagado']:,.2f}",
            f"Pendiente: {moneda} {payment['monto_pendiente']:,.2f}",
            f"Estado: {payment['estado'].upper()}",
            f"Vence: {payment['fecha_vencimiento'][:10]}",
        ]
        
        if payment["transacciones"]:
            lines.append("\n**Transacciones:**")
            for t in payment["transacciones"]:
                lines.append(f"  • {t['fecha'][:10]}: {moneda} {t['monto']:,.2f} ({t['metodo']})")
        
        return "\n".join(lines)
    
    def format_overdue(self, payments: List[Dict[str, Any]]) -> str:
        """Format overdue payments alert."""
        if not payments:
            return "✅ No hay pagos vencidos."
        
        moneda = self.config.moneda
        lines = [f"⚠️ **Pagos Vencidos ({len(payments)})**\n"]
        
        for p in payments:
            dias = p.get("_dias_vencido", 0)
            emoji = "🔴" if dias > 14 else "🟡"
            tipo_label = "Por cobrar" if p["tipo"] == "ingreso" else "Por pagar"
            
            lines.append(f"{emoji} **{p['concepto']}** — {p['cliente_nombre']}")
            lines.append(f"   {tipo_label}: {moneda} {p['monto_pendiente']:,.2f} (vencido {dias} días)")
            lines.append("")
        
        return "\n".join(lines)


# Singleton
_pagos_instance = None


def get_pagos() -> Pagos:
    """Get or create singleton Pagos instance."""
    global _pagos_instance
    if _pagos_instance is None:
        _pagos_instance = Pagos()
    return _pagos_instance
