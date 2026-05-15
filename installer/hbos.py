#!/usr/bin/env python3
"""
Hermes Business OS — CLI Installer
Entry point for all HBOS commands.
"""

import sys
import argparse
from pathlib import Path

# Add installer modules to path
INSTALLER_DIR = Path(__file__).parent
sys.path.insert(0, str(INSTALLER_DIR))

from install import InstallCommand
from setup_wizard import SetupWizard
from doctor import DoctorCommand


def main():
    parser = argparse.ArgumentParser(
        description="Hermes Business OS — Installer & Manager",
        prog="hbos"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install HBOS skills into Hermes")
    install_parser.add_argument("--profile", default="default", help="Hermes profile name")
    install_parser.add_argument("--path", help="Path to HBOS directory")
    
    # Setup wizard
    setup_parser = subparsers.add_parser("setup", help="Run interactive setup wizard")
    setup_parser.add_argument("--non-interactive", action="store_true", help="Skip interactive prompts")
    
    # Doctor
    doctor_parser = subparsers.add_parser("doctor", help="Diagnose HBOS installation")
    
    # Update
    update_parser = subparsers.add_parser("update", help="Update HBOS to latest version")
    
    # Status
    status_parser = subparsers.add_parser("status", help="Show HBOS status")
    
    args = parser.parse_args()
    
    if args.command == "install":
        cmd = InstallCommand(profile=args.profile, path=args.path)
        cmd.run()
    elif args.command == "setup":
        wizard = SetupWizard(non_interactive=args.non_interactive)
        wizard.run()
    elif args.command == "doctor":
        cmd = DoctorCommand()
        cmd.run()
    elif args.command == "update":
        print("🔄 Update command coming soon...")
    elif args.command == "status":
        show_status()
    else:
        parser.print_help()
        sys.exit(1)


def show_status():
    """Show current HBOS installation status."""
    print("\n🏢 Hermes Business OS Status")
    print("=" * 40)
    
    # Check Hermes installation
    hermes_home = Path.home() / ".hermes"
    if hermes_home.exists():
        print(f"✅ Hermes Agent installed: {hermes_home}")
    else:
        print(f"❌ Hermes Agent not found")
        print(f"   Install with: curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash")
    
    # Check HBOS skills
    hbos_dir = Path(__file__).parent.parent
    skills_dir = hbos_dir / "skills"
    if skills_dir.exists():
        skills = [d.name for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith("__")]
        print(f"✅ HBOS skills found: {len(skills)}")
        for skill in sorted(skills):
            print(f"   • {skill}")
    
    # Check config
    config_file = hbos_dir / "config" / "empresa.yaml"
    if config_file.exists():
        print(f"✅ Company config: {config_file}")
    else:
        print(f"⚠️  Company config not found. Run: hbos setup")
    
    print()


if __name__ == "__main__":
    main()
