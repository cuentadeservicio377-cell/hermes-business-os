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
run_test "HBOS CLI exists" "test -f '$PROJECT_DIR/installer/hbos.py'"

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

echo ""
echo "4. Template Tests"
echo "-----------------"

run_test "Base template" "test -f '$PROJECT_DIR/skills/hermes-documentos/tools/templates/default/base.html'"
run_test "Eventos cotizacion template" "test -f '$PROJECT_DIR/skills/hermes-documentos/tools/templates/eventos/cotizacion.html'"
run_test "Legal propuesta template" "test -f '$PROJECT_DIR/skills/hermes-documentos/tools/templates/legal/propuesta-honorarios.html'"
run_test "Consultoria propuesta template" "test -f '$PROJECT_DIR/skills/hermes-documentos/tools/templates/consultoria/propuesta-consultoria.html'"
run_test "Retail cotizacion template" "test -f '$PROJECT_DIR/skills/hermes-documentos/tools/templates/retail/cotizacion.html'"

echo ""
echo "5. Documentation Tests"
echo "----------------------"

run_test "INSTALL.md" "test -f '$PROJECT_DIR/docs/INSTALL.md'"
run_test "USER-GUIDE.md" "test -f '$PROJECT_DIR/docs/USER-GUIDE.md'"

echo ""
echo "6. Functional Tests"
echo "-------------------"

run_test "CRM add client" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-ventas/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from crm import CRM; c = CRM(); import time; nombre = \"Test_\" + str(int(time.time())); result = c.add_client(nombre, email=\"test@test.com\"); assert result[\"success\"]; print(result[\"cliente\"][\"id\"])
'"

run_test "Cotizador calculate" "python3 -c '
import sys; sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-ventas/tools\"); sys.path.insert(0, \"$PROJECT_DIR/skills/hermes-business-core/tools\");
from cotizador import Cotizador; cot = Cotizador(); result = cot.calculate_quote([{\"codigo\": \"CON-DIA\", \"cantidad\": 1}]); assert result[\"total\"] > 0; print(result[\"total\"])
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
