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
    
    # Onboarding
    onboarding_parser = subparsers.add_parser("onboarding", help="Run full onboarding (setup + data + Google Workspace)")
    onboarding_parser.add_argument("--config", help="Path to empresa.yaml")
    onboarding_parser.add_argument("--skip-gw", action="store_true", help="Skip Google Workspace setup")
    
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
    elif args.command == "onboarding":
        run_onboarding(args)
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


def run_onboarding(args):
    """Run the full onboarding process."""
    print("\n🏢 Hermes Business OS — Onboarding Completo\n")
    
    # Step 1: Setup wizard if no config
    config_path = Path(args.config) if args.config else None
    
    if not config_path or not config_path.exists():
        existing_config = Path(__file__).parent.parent / "config" / "empresa.yaml"
        if not existing_config.exists():
            print("⚠️  No se encontró configuración. Iniciando setup wizard...\n")
            wizard = SetupWizard()
            wizard.run()
        else:
            print("✅ Configuración existente encontrada.\n")
    
    # Step 2: Run onboarding engine
    sys.path.insert(0, str(Path(__file__).parent.parent / "skills" / "hermes-business-core" / "tools"))
    from onboarding_engine import OnboardingEngine
    
    engine = OnboardingEngine(config_path=str(config_path) if config_path else None)
    
    if args.skip_gw:
        # Disable Google Workspace in config temporarily
        config = engine.config
        if hasattr(config, '_config'):
            config._config.setdefault("integraciones", {}).setdefault("google_workspace", {})["activo"] = False
    
    result = engine.run_full_onboarding()
    
    print("\n" + "=" * 50)
    if result["success"] and not result["errors"]:
        print("✅ Onboarding completado exitosamente")
    elif result["success"]:
        print("✅ Onboarding completado con advertencias")
    else:
        print("❌ Onboarding completado con errores")
    
    print("\nResumen de pasos:")
    for step in result["steps"]:
        emoji = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}.get(step["status"], "•")
        print(f"  {emoji} {step['message']}")
    
    if result["errors"]:
        print("\nErrores:")
        for err in result["errors"]:
            print(f"  ❌ {err}")
    
    print("\n" + "=" * 50)
    print("\n🚀 Próximos pasos:")
    print("  1. Revisa tu config: config/empresa.yaml")
    print("  2. Abre el dashboard: cd dashboard && npm install && npm run dev")
    print("  3. Inicia Hermes: hermes gateway start")
    print("  4. Habla con tu bot en Telegram")
    print()


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
    
    # Check onboarding status
    sys.path.insert(0, str(hbos_dir / "skills" / "hermes-business-core" / "tools"))
    try:
        from onboarding_engine import OnboardingEngine
        engine = OnboardingEngine()
        status = engine.get_onboarding_status()
        
        print(f"\n📋 Onboarding Status:")
        print(f"   Empresa: {status['company_name']}")
        print(f"   Industria: {status['industry']}")
        print(f"   Departamentos: {', '.join(status['departments_active'])}")
        print(f"   Google Workspace: {'✅' if status['google_workspace_active'] else '❌'}")
    except Exception as e:
        print(f"\n⚠️  No se pudo cargar onboarding engine: {e}")
    
    print()


if __name__ == "__main__":
    main()
