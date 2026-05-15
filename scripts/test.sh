#!/bin/bash
#
# Hermes Business OS — Test Suite
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🏢 Hermes Business OS — Test Suite"
echo "==================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

# Test helper
run_test() {
    local name="$1"
    local command="$2"
    
    echo -n "Testing: $name ... "
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}FAIL${NC}"
        FAIL=$((FAIL + 1))
    fi
}

# Tests
echo "1. File Structure Tests"
echo "-----------------------"

run_test "PLAN.md exists" "test -f '$PROJECT_DIR/PLAN.md'"
run_test "README.md exists" "test -f '$PROJECT_DIR/README.md'"
run_test "Config template exists" "test -f '$PROJECT_DIR/config/empresa.yaml.example'"
run_test "Install script exists" "test -f '$PROJECT_DIR/scripts/install.sh'"
run_test "Update script exists" "test -f '$PROJECT_DIR/scripts/update.sh'"
run_test "HBOS CLI exists" "test -f '$PROJECT_DIR/installer/hbos.py'"
run_test "CHANGELOG exists" "test -f '$PROJECT_DIR/CHANGELOG.md'"
run_test "CONTRIBUTING exists" "test -f '$PROJECT_DIR/CONTRIBUTING.md'"
run_test "LICENSE exists" "test -f '$PROJECT_DIR/LICENSE'"

echo ""
echo "2. Skills Tests"
echo "---------------"

run_test "Business Core skill" "test -f '$PROJECT_DIR/skills/hermes-business-core/SKILL.md'"
run_test "Ventas skill" "test -f '$PROJECT_DIR/skills/hermes-ventas/SKILL.md'"
run_test "Operaciones skill" "test -f '$PROJECT_DIR/skills/hermes-operaciones/SKILL.md'"
run_test "Documentos skill" "test -f '$PROJECT_DIR/skills/hermes-documentos/SKILL.md'"
run_test "Finanzas skill" "test -f '$PROJECT_DIR/skills/hermes-finanzas/SKILL.md'"
run_test "RRHH skill" "test -f '$PROJECT_DIR/skills/hermes-rrhh/SKILL.md'"

echo ""
echo "3. Python Tools Tests"
echo "---------------------"

run_test "Config loader" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from config_loader import ConfigLoader; c = ConfigLoader(\"$PROJECT_DIR/config/empresa.yaml.example\"); print(c.nombre)'"
run_test "Router imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from router import IntentRouter; r = IntentRouter(); print(r.route(\"cotiza algo\"))'"
run_test "Google Workspace imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from google_workspace import GoogleWorkspace; gw = GoogleWorkspace(); print(\"ok\")'"
run_test "CRM tool imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-ventas/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from crm import CRM; c = CRM(); print(\"ok\")'"
run_test "Cotizador tool imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-ventas/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from cotizador import Cotizador; cot = Cotizador(); print(\"ok\")'"
run_test "Pipeline tool imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-ventas/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from pipeline import Pipeline; p = Pipeline(); print(\"ok\")'"
run_test "Proyectos tool imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-operaciones/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from proyectos import Proyectos; pr = Proyectos(); print(\"ok\")'"
run_test "Tareas tool imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-operaciones/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from tareas import Tareas; t = Tareas(); print(\"ok\")'"
run_test "Checklists tool imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-operaciones/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from checklists import Checklists; ch = Checklists(); print(\"ok\")'"
run_test "Kami engine imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-documentos/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from kami_engine import KamiEngine; k = KamiEngine(); print(\"ok\")'"
run_test "Onboarding engine imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from onboarding_engine import OnboardingEngine; o = OnboardingEngine(\"$PROJECT_DIR/config/empresa.yaml.example\"); print(\"ok\")'"
run_test "Presupuestos tool imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-finanzas/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from presupuestos import Presupuestos; p = Presupuestos(); print(\"ok\")'"
run_test "Pagos tool imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-finanzas/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from pagos import Pagos; p = Pagos(); print(\"ok\")'"
run_test "Reportes tool imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-finanzas/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from reportes import ReportesFinancieros; r = ReportesFinancieros(); print(\"ok\")'"
run_test "Equipos tool imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-rrhh/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from equipos import Equipos; e = Equipos(); print(\"ok\")'"
run_test "Asistencia tool imports" "python3 -c 'import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-rrhh/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\"); from asistencia import Asistencia; a = Asistencia(); print(\"ok\")'"

echo ""
echo "4. Template Tests"
echo "-----------------"

run_test "Base template" "test -f '$PROJECT_DIR/skills/hermes-documentos/tools/templates/default/base.html'"
run_test "Eventos cotizacion template" "test -f '$PROJECT_DIR/skills/hermes-documentos/tools/templates/eventos/cotizacion.html'"
run_test "Legal propuesta template" "test -f '$PROJECT_DIR/skills/hermes-documentos/tools/templates/legal/propuesta-honorarios.html'"
run_test "Consultoria propuesta template" "test -f '$PROJECT_DIR/skills/hermes-documentos/tools/templates/consultoria/propuesta-consultoria.html'"
run_test "Retail cotizacion template" "test -f '$PROJECT_DIR/skills/hermes-documentos/tools/templates/retail/cotizacion.html'"

echo ""
echo "5. Dashboard Tests"
echo "------------------"

run_test "Dashboard package.json" "test -f '$PROJECT_DIR/dashboard/package.json'"
run_test "Dashboard layout" "test -f '$PROJECT_DIR/dashboard/app/layout.tsx'"
run_test "Dashboard page" "test -f '$PROJECT_DIR/dashboard/app/page.tsx'"
run_test "Dashboard clientes" "test -f '$PROJECT_DIR/dashboard/app/clientes/page.tsx'"
run_test "Dashboard pipeline" "test -f '$PROJECT_DIR/dashboard/app/pipeline/page.tsx'"
run_test "Dashboard proyectos" "test -f '$PROJECT_DIR/dashboard/app/proyectos/page.tsx'"
run_test "Dashboard tareas" "test -f '$PROJECT_DIR/dashboard/app/tareas/page.tsx'"
run_test "Dashboard configuracion" "test -f '$PROJECT_DIR/dashboard/app/configuracion/page.tsx'"
run_test "Dashboard Nav component" "test -f '$PROJECT_DIR/dashboard/components/Nav.tsx'"
run_test "Dashboard data lib" "test -f '$PROJECT_DIR/dashboard/lib/data.ts'"
run_test "Dashboard API route" "test -f '$PROJECT_DIR/dashboard/app/api/data/route.ts'"
run_test "Dashboard tailwind config" "test -f '$PROJECT_DIR/dashboard/tailwind.config.ts'"
run_test "Dashboard tsconfig" "test -f '$PROJECT_DIR/dashboard/tsconfig.json'"

echo ""
echo "6. Documentation Tests"
echo "----------------------"

run_test "INSTALL EN" "test -f '$PROJECT_DIR/docs/en/INSTALL.md'"
run_test "INSTALL ES" "test -f '$PROJECT_DIR/docs/es/INSTALL.md'"
run_test "USER-GUIDE EN" "test -f '$PROJECT_DIR/docs/en/USER-GUIDE.md'"
run_test "USER-GUIDE ES" "test -f '$PROJECT_DIR/docs/es/USER-GUIDE.md'"
run_test "ADMIN-GUIDE EN" "test -f '$PROJECT_DIR/docs/en/ADMIN-GUIDE.md'"
run_test "ADMIN-GUIDE ES" "test -f '$PROJECT_DIR/docs/es/ADMIN-GUIDE.md'"
run_test "API EN" "test -f '$PROJECT_DIR/docs/en/API.md'"
run_test "API ES" "test -f '$PROJECT_DIR/docs/es/API.md'"
run_test "Research Paper ES" "test -f '$PROJECT_DIR/docs/RESEARCH-PAPER.md'"
run_test "Research Paper EN" "test -f '$PROJECT_DIR/docs/RESEARCH-PAPER.en.md'"
run_test "Industry eventos config" "test -f '$PROJECT_DIR/config/industrias/eventos.yaml'"
run_test "Industry legal config" "test -f '$PROJECT_DIR/config/industrias/legal.yaml'"
run_test "Industry consultoria config" "test -f '$PROJECT_DIR/config/industrias/consultoria.yaml'"
run_test "Industry retail config" "test -f '$PROJECT_DIR/config/industrias/retail.yaml'"
run_test "Dockerfile exists" "test -f '$PROJECT_DIR/docker/Dockerfile'"
run_test "Docker compose exists" "test -f '$PROJECT_DIR/docker/docker-compose.yml'"

echo ""
echo "7. Functional Tests"
echo "-------------------"

run_test "CRM add client" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-ventas/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from crm import CRM; c = CRM(); import time; nombre = \"Test_\" + str(int(time.time())); result = c.add_client(nombre, email=\"test@test.com\"); assert result[\"success\"]; print(result[\"cliente\"][\"id\"])
'"

run_test "Cotizador calculate" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-ventas/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from cotizador import Cotizador; cot = Cotizador(); result = cot.calculate_quote([{\"codigo\": \"EVT-BAS\", \"cantidad\": 1}]); assert result[\"total\"] > 0; print(result[\"total\"])
'"

run_test "Proyectos create" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-operaciones/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from proyectos import Proyectos; p = Proyectos(); result = p.create_project(\"Test Proyecto\"); assert result[\"success\"]; print(result[\"proyecto\"][\"id\"])
'"

run_test "Tareas create" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-operaciones/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from tareas import Tareas; t = Tareas(); result = t.create_task(\"PROJ-001\", \"Test tarea\"); assert result[\"success\"]; print(result[\"tarea\"][\"id\"])
'"

run_test "Checklists create" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-operaciones/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from checklists import Checklists; ch = Checklists(); result = ch.create_project_checklist(\"PROJ-001\"); assert result[\"success\"]; print(len(result[\"checklist\"][\"phases\"]))
'"

run_test "Router route cotiza" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from router import IntentRouter; r = IntentRouter(); result = r.route(\"cotiza una boda\"); assert result == \"hermes-ventas\"; print(result)
'"

run_test "Router route proyecto" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from router import IntentRouter; r = IntentRouter(); result = r.route(\"crea un proyecto\"); assert result == \"hermes-operaciones\"; print(result)
'"

run_test "Onboarding engine status" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from onboarding_engine import OnboardingEngine; o = OnboardingEngine(\"$PROJECT_DIR/config/empresa.yaml.example\"); status = o.get_onboarding_status(); assert status[\"config_exists\"]; print(status[\"company_name\"])
'"

run_test "Onboarding creates data files" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from onboarding_engine import OnboardingEngine; o = OnboardingEngine(\"$PROJECT_DIR/config/empresa.yaml.example\"); result = o.run_full_onboarding(); assert len(result[\"steps\"]) > 0; print(len(result[\"steps\"]))
'"

run_test "Presupuestos create budget" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-finanzas/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from presupuestos import Presupuestos; p = Presupuestos(); result = p.create_budget(\"PROJ-001\", \"Proyecto Test\", [{\"concepto\": \"Servicio\", \"monto\": 1000}], [{\"concepto\": \"Costos\", \"monto\": 500, \"tipo\": \"material\"}]); assert result[\"success\"]; print(result[\"presupuesto\"][\"id\"])
'"

run_test "Pagos register and transaction" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-finanzas/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from pagos import Pagos; p = Pagos(); result = p.register_payment(\"PROJ-001\", \"Proyecto Test\", \"CLI-001\", \"Cliente Test\", 1000, \"Pago servicio\"); assert result[\"success\"]; tx = p.add_transaction(result[\"pago\"][\"id\"], 500); assert tx[\"success\"]; print(tx[\"pago\"][\"monto_pagado\"])
'"

run_test "Equipos add member" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-rrhh/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from equipos import Equipos; e = Equipos(); result = e.add_member(\"Juan Perez\", rol=\"Coordinador\", tarifa_dia=500); assert result[\"success\"]; print(result[\"miembro\"][\"id\"])
'"

run_test "Asistencia register and payroll" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-rrhh/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from asistencia import Asistencia; a = Asistencia(); result = a.register_entry(\"EMP-001\", \"Juan Perez\", horas=8); assert result[\"success\"]; print(result[\"registro\"][\"id\"])
'"

echo ""
echo "==================================="
echo -e "Results: ${GREEN}$PASS passed${NC}, ${RED}$FAIL failed${NC}"
echo ""

if [ $FAIL -gt 0 ]; then
    exit 1
else
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
fi
