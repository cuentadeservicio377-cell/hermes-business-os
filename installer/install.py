"""
Hermes Business OS — Install Command
Installs HBOS skills into an existing Hermes Agent installation.
"""

import shutil
import sys
from pathlib import Path


class InstallCommand:
    """Handles installation of HBOS skills into Hermes."""
    
    def __init__(self, profile: str = "default", path: str = None):
        self.profile = profile
        self.hbos_path = Path(path) if path else Path(__file__).parent.parent
        self.hermes_home = Path.home() / ".hermes"
        self.skills_target = self.hermes_home / "skills"
        
    def run(self):
        """Execute installation."""
        print("🏢 Hermes Business OS — Installer\n")
        
        # Pre-flight checks
        if not self._check_hermes():
            return False
            
        # Install skills
        self._install_skills()
        
        # Copy config template
        self._copy_config()
        
        print("\n✅ Installation complete!")
        print("\nNext steps:")
        print("  1. Run: hbos setup")
        print("  2. Configure your company in config/empresa.yaml")
        print("  3. Start Hermes: hermes gateway start")
        
        return True
    
    def _check_hermes(self) -> bool:
        """Check if Hermes Agent is installed."""
        if not self.hermes_home.exists():
            print("❌ Hermes Agent not found.")
            print("   Please install Hermes first:")
            print("   curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash")
            return False
        
        print(f"✅ Hermes Agent found: {self.hermes_home}")
        return True
    
    def _install_skills(self):
        """Copy HBOS skills to Hermes skills directory."""
        skills_source = self.hbos_path / "skills"
        if not skills_source.exists():
            print(f"❌ Skills directory not found: {skills_source}")
            return
        
        self.skills_target.mkdir(parents=True, exist_ok=True)
        
        installed = 0
        for skill_dir in skills_source.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith("__"):
                target = self.skills_target / skill_dir.name
                
                # Remove existing skill if present
                if target.exists():
                    shutil.rmtree(target)
                
                # Copy skill
                shutil.copytree(skill_dir, target)
                installed += 1
                print(f"  ✅ Installed: {skill_dir.name}")
        
        print(f"\n📦 {installed} skills installed to: {self.skills_target}")
    
    def _copy_config(self):
        """Copy config template if not exists."""
        config_source = self.hbos_path / "config" / "empresa.yaml.example"
        config_target = self.hbos_path / "config" / "empresa.yaml"
        
        if config_source.exists() and not config_target.exists():
            shutil.copy2(config_source, config_target)
            print(f"\n📋 Config template copied to: {config_target}")
