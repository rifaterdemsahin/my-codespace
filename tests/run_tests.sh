#!/usr/bin/env bash
# ==============================================================================
# Automated Test Runner for Local & Cloud Codespace
# ==============================================================================
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}==============================================${NC}"
echo -e "${BLUE}  Running Codespace Environment Test Suite    ${NC}"
echo -e "${BLUE}==============================================${NC}"

ERRORS=0

run_check() {
    local title="$1"
    local cmd="$2"
    echo -n "Checking: ${title}... "
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "${GREEN}[PASS]${NC}"
    else
        echo -e "${RED}[FAIL]${NC}"
        ERRORS=$((ERRORS + 1))
    fi
}

# 1. Devcontainer Configuration
run_check "devcontainer.json exists" "[ -f .devcontainer/devcontainer.json ]"
run_check "devcontainer.json valid JSON" "python3 -c 'import json; json.load(open(\".devcontainer/devcontainer.json\"))'"
run_check "devcontainer forwards port 8080" "python3 -c 'import json; assert 8080 in json.load(open(\".devcontainer/devcontainer.json\"))[\"forwardPorts\"]'"

# 2. Docker & Container Service
run_check "Docker daemon active" "sudo docker info"
run_check "Container 'my-codespace-local' is running" "[ \$(sudo docker inspect -f '{{.State.Running}}' my-codespace-local 2>/dev/null) = 'true' ]"
run_check "Container mounts project workspace" "sudo docker exec my-codespace-local test -f /home/coder/project/README.md"

# 3. HTTP Endpoints & Web Workbench
run_check "HTTP port 8080 open and responding" "curl -sI --max-time 3 http://localhost:8080"
run_check "HTTP redirects directly to project (auth disabled)" "curl -sI http://localhost:8080 | grep -q 'Location: ./?folder=/home/coder/project'"
run_check "VS Code Web Workbench HTML serves 200 OK" "curl -sL http://localhost:8080 | grep -q 'vscode-workbench'"

echo ""
echo -e "${BLUE}--- Running Python Unit Tests ---${NC}"
if python3 tests/test_codespace.py; then
    echo -e "${GREEN}Python unit tests completed successfully!${NC}"
else
    echo -e "${RED}Python unit tests failed!${NC}"
    ERRORS=$((ERRORS + 1))
fi

echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo -e "${GREEN}==============================================${NC}"
    echo -e "${GREEN}  ALL TESTS PASSED! Environment is 100% healthy.${NC}"
    echo -e "${GREEN}==============================================${NC}"
    exit 0
else
    echo -e "${RED}==============================================${NC}"
    echo -e "${RED}  $ERRORS TEST(S) FAILED. Check the output above. ${NC}"
    echo -e "${RED}==============================================${NC}"
    exit 1
fi
