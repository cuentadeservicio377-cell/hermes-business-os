#!/bin/bash
#
# Hermes Business OS — Installer Script
# One-liner install for macOS and Linux
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/cuentadeservicio377-cell/hermes-business-os/main/scripts/install.sh | bash
#

set -e

HBOS_VERSION="2.0.0"
HBOS_REPO="https://github.com/cuentadeservicio377-cell/hermes-business-os"
INSTALL_DIR="${HOME}/.hermes-business-os"
HERMES_HOME="${HOME}/.hermes"

echo "🏢 Hermes Business OS v${HBOS_VERSION} — Installer"
echo "================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Hermes is installed
check_hermes() {
    if [ ! -d "$HERMES_HOME" ]; then
        echo -e "${RED}❌ Hermes Agent not found.${NC}"
        echo ""
        echo "Hermes Business OS requires Hermes Agent to be installed first."
        echo ""
        echo "Install Hermes Agent:"
        echo "  curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash"
        echo ""
        exit 1
    fi
    echo -e "${GREEN}✅ Hermes Agent found${NC}"
}

# Check Python
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 not found${NC}"
        echo "Please install Python 3.11 or higher."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo -e "${GREEN}✅ Python ${PYTHON_VERSION} found${NC}"
}

# Clone or update repository
clone_repo() {
    if [ -d "$INSTALL_DIR" ]; then
        echo -e "${YELLOW}⚠️  HBOS already installed at ${INSTALL_DIR}${NC}"
        echo "Updating to latest version..."
        cd "$INSTALL_DIR"
        git pull origin main || true
    else
        echo "📥 Cloning repository..."
        git clone --depth 1 "$HBOS_REPO" "$INSTALL_DIR"
    fi
}

# Install HBOS skills
install_skills() {
    echo ""
    echo "📦 Installing skills..."
    
    SKILLS_SOURCE="${INSTALL_DIR}/skills"
    SKILLS_TARGET="${HERMES_HOME}/skills"
    
    mkdir -p "$SKILLS_TARGET"
    
    # Count skills
    SKILL_COUNT=0
    for skill_dir in "$SKILLS_SOURCE"/*/; do
        if [ -d "$skill_dir" ]; then
            skill_name=$(basename "$skill_dir")
            
            # Remove existing skill
            if [ -d "${SKILLS_TARGET}/${skill_name}" ]; then
                rm -rf "${SKILLS_TARGET}/${skill_name}"
            fi
            
            # Copy skill
            cp -r "$skill_dir" "${SKILLS_TARGET}/"
            echo "  ✅ ${skill_name}"
            SKILL_COUNT=$((SKILL_COUNT + 1))
        fi
    done
    
    echo ""
    echo -e "${GREEN}📦 ${SKILL_COUNT} skills installed${NC}"
}

# Copy config template
copy_config() {
    CONFIG_SOURCE="${INSTALL_DIR}/config/empresa.yaml.example"
    CONFIG_TARGET="${INSTALL_DIR}/config/empresa.yaml"
    
    if [ ! -f "$CONFIG_TARGET" ]; then
        cp "$CONFIG_SOURCE" "$CONFIG_TARGET"
        echo -e "${GREEN}📋 Config template created${NC}"
    else
        echo -e "${YELLOW}📋 Config already exists, keeping existing${NC}"
    fi
}

# Install Python dependencies
install_deps() {
    echo ""
    echo "📦 Installing Python dependencies..."
    
    # Check if pip is available
    if ! command -v pip3 &> /dev/null; then
        echo -e "${YELLOW}⚠️  pip3 not found. Some features may not work.${NC}"
        echo "Run: python3 -m ensurepip --upgrade"
        return
    fi
    
    # Install required packages
    pip3 install --user pyyaml google-api-python-client google-auth-httplib2 google-auth-oauthlib weasyprint 2>/dev/null || {
        echo -e "${YELLOW}⚠️  Some dependencies could not be installed.${NC}"
        echo "You may need to install them manually."
    }
}

# Create symlink for hbos command
create_symlink() {
    HBOS_BIN="${INSTALL_DIR}/installer/hbos.py"
    LOCAL_BIN="${HOME}/.local/bin/hbos"
    
    mkdir -p "${HOME}/.local/bin"
    
    # Make executable
    chmod +x "$HBOS_BIN"
    
    # Create symlink
    if [ -L "$LOCAL_BIN" ]; then
        rm "$LOCAL_BIN"
    fi
    
    ln -s "$HBOS_BIN" "$LOCAL_BIN" || true
    
    # Add to PATH if needed
    if [[ ":$PATH:" != *":${HOME}/.local/bin:"* ]]; then
        echo ""
        echo -e "${YELLOW}⚠️  ~/.local/bin is not in your PATH${NC}"
        echo "Add this to your shell profile:"
        echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    fi
    
    echo -e "${GREEN}✅ hbos command installed${NC}"
}

# Main installation
main() {
    check_hermes
    check_python
    clone_repo
    install_skills
    copy_config
    install_deps
    create_symlink
    
    echo ""
    echo "================================================"
    echo -e "${GREEN}✅ Hermes Business OS v${HBOS_VERSION} installed successfully!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Configure your company: hbos setup"
    echo "  2. Review config: ${INSTALL_DIR}/config/empresa.yaml"
    echo "  3. Set up Google Workspace (optional)"
    echo "  4. Start Hermes: hermes gateway start"
    echo "  5. Talk to your bot on Telegram!"
    echo ""
    echo "Documentation: ${INSTALL_DIR}/docs/"
    echo ""
}

main "$@"
