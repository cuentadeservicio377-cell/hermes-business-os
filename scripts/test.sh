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
NC='\033[0m'

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

echo ""
echo "4. Documentation Tests"
echo "----------------------"

run_test "INSTALL.md" "test -f '$PROJECT_DIR/docs/INSTALL.md'"
run_test "USER-GUIDE.md" "test -f '$PROJECT_DIR/docs/USER-GUIDE.md'"

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
