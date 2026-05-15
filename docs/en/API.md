# API Reference — Hermes Business OS Tools

Reference for all Python tools available in HBOS skills.

---

## hermes-business-core

### `config_loader.ConfigLoader`

```python
from config_loader import ConfigLoader

config = ConfigLoader("config/empresa.yaml")
config.nombre          # str — Nombre de la empresa
config.industria       # str — Industria
config.moneda          # str — Moneda (e.g., "MXN")
config.departamentos   # List[str] — Departamentos activos
config.integracion_activa("google_workspace")  # bool
```

### `router.IntentRouter`

```python
from router import IntentRouter

router = IntentRouter()
skill = router.route("cotiza una boda")  # "hermes-ventas"
skill = router.route("crea proyecto")    # "hermes-operaciones"
```

### `google_workspace.GoogleWorkspace`

```python
from google_workspace import GoogleWorkspace

gw = GoogleWorkspace()
gw.create_drive_folder("Clientes")
gw.create_sheet("Índice de Proyectos")
```

### `onboarding_engine.OnboardingEngine`

```python
from onboarding_engine import OnboardingEngine

engine = OnboardingEngine("config/empresa.yaml")
engine.run_full_onboarding()   # Dict with results
engine.get_onboarding_status() # Dict with status
```

---

## hermes-ventas

### `crm.CRM`

```python
from crm import get_crm

crm = get_crm()
crm.add_client("Juan Pérez", email="juan@example.com")
crm.find_client("Juan")
crm.get_pipeline_summary()
```

**Methods:**
- `add_client(nombre, **kwargs)` → `Dict`
- `find_client(query)` → `Optional[Dict]`
- `update_status(client_id, status)` → `Dict`
- `get_pipeline_summary()` → `Dict`
- `extract_client_from_message(text)` → `Dict`

### `cotizador.Cotizador`

```python
from cotizador import get_cotizador

cot = get_cotizador()
cot.calculate_quote(
    items=[{"codigo": "EVT-BAS", "cantidad": 1}],
    multiplicador=1.2,
    descuento=0.1
)
cot.get_catalogo("eventos")
```

### `pipeline.Pipeline`

```python
from pipeline import get_pipeline

pipe = get_pipeline()
pipe.add_deal("CLI-001", "Boda Juan", 250000)
pipe.move_deal("DEAL-001", "propuesta")
pipe.get_forecast()
```

---

## hermes-operaciones

### `proyectos.Proyectos`

```python
from proyectos import get_proyectos

pr = get_proyectos()
pr.create_project("Boda Juan", cliente_id="CLI-001")
pr.update_status("PROJ-001", "en_progreso")
pr.update_progress("PROJ-001", 50)
```

### `tareas.Tareas`

```python
from tareas import get_tareas

t = get_tareas()
t.create_task("PROJ-001", "Confirmar lugar")
t.complete_task("TASK-001")
t.get_overdue_tasks()
```

### `checklists.Checklists`

```python
from checklists import get_checklists

ch = get_checklists()
ch.create_project_checklist("PROJ-001")
ch.create_industry_checklist("PROJ-001", "eventos")
```

---

## hermes-documentos

### `kami_engine.KamiEngine`

```python
from kami_engine import KamiEngine

kami = KamiEngine()
kami.list_templates()
kami.render_template("eventos/cotizacion.html", {"cliente": {...}})
kami.generate_pdf("eventos/cotizacion.html", variables, "output.pdf")
```

---

## hermes-finanzas

### `presupuestos.Presupuestos`

```python
from presupuestos import get_presupuestos

p = get_presupuestos()
p.create_budget(
    proyecto_id="PROJ-001",
    proyecto_nombre="Boda Juan",
    ingresos=[{"concepto": "Servicio", "monto": 1000}],
    costos=[{"concepto": "Material", "monto": 500, "tipo": "material"}],
    margen_esperado=30
)
p.approve_budget("PRE-001")
p.get_financial_summary()
```

### `pagos.Pagos`

```python
from pagos import get_pagos

pg = get_pagos()
pg.register_payment(
    proyecto_id="PROJ-001",
    proyecto_nombre="Boda Juan",
    cliente_id="CLI-001",
    cliente_nombre="Juan Pérez",
    monto_total=250000,
    concepto="Anticipo boda"
)
pg.add_transaction("PAG-001", 125000, metodo="transferencia")
pg.get_overdue_payments()
pg.get_payment_summary()
```

### `reportes.ReportesFinancieros`

```python
from reportes import get_reportes

r = get_reportes()
r.generate_monthly_report(year=2025, month=5)
r.generate_cash_flow(months=6)
r.generate_project_report("PROJ-001")
```

---

## hermes-rrhh

### `equipos.Equipos`

```python
from equipos import get_equipos

e = get_equipos()
e.add_member("María López", rol="Coordinador", tarifa_dia=800)
e.assign_to_project("EMP-001", "PROJ-001")
e.get_team_summary()
```

### `asistencia.Asistencia`

```python
from asistencia import get_asistencia

a = get_asistencia()
a.register_entry("EMP-001", "María López", horas=8, proyecto_id="PROJ-001")
a.calculate_payroll(
    member_id="EMP-001",
    member_nombre="María López",
    tarifa_dia=800,
    fecha_inicio="2025-05-01",
    fecha_fin="2025-05-15"
)
```

---

## Data Persistence

All tools write to `data/*.json`. The data directory is created automatically on first use.

```
data/
├── clients.json
├── quotes.json
├── pipeline.json
├── projects.json
├── tasks.json
├── checklists.json
├── budgets.json
├── payments.json
├── team.json
├── attendance.json
└── catalog.json
```

---

## Singleton Pattern

All tools follow a singleton pattern:

```python
# Correct — reuses instance
crm = get_crm()

# Also correct but creates new instance
crm = CRM()
```

Use `get_*()` functions in production to ensure data consistency.
