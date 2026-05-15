#!/bin/bash
#
# Hermes Business OS — Update Script
# Updates HBOS to the latest version from the git repository.
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
INSTALL_DIR="${HOME}/.hermes-business-os"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔄 Hermes Business OS — Updater${NC}"
echo "================================"
echo ""

# Check if installed via git
if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Updating from git repository..."
    cd "$INSTALL_DIR"
    
    # Stash local changes if any
    if ! git diff --quiet HEAD 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Local changes detected. Stashing...${NC}"
        git stash
    fi
    
    git pull origin main
    
    # Reinstall skills
    echo "Reinstalling skills..."
    if command -v hbos &> /dev/null; then
        hbos install --path "$INSTALL_DIR"
    else
        echo -e "${YELLOW}⚠️  hbos not found. Run 'hbos install' manually.${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}✅ Update complete!${NC}"
    
elif [ -d "$PROJECT_DIR/.git" ]; then
    echo "Development mode detected. Pulling latest changes..."
    cd "$PROJECT_DIR"
    git pull origin main
    echo -e "${GREEN}✅ Repository updated. Run tests: bash scripts/test.sh${NC}"
    
else
    echo -e "${RED}❌ Not a git installation.${NC}"
    echo "Reinstall with:"
    echo "  curl -fsSL https://raw.githubusercontent.com/cuentadeservicio377-cell/hermes-business-os/main/scripts/install.sh | bash"
    exit 1
fi

# Verify
if command -v hbos &> /dev/null; then
    echo ""
    hbos status
fi

echo ""
echo -e "${GREEN}🎉 Hermes Business OS is up to date!${NC}"
