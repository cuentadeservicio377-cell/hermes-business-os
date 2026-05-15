"""
Hermes Business OS — Doctor Command
Diagnoses the HBOS installation and reports issues.
"""

import sys
from pathlib import Path


class DoctorCommand:
    """Diagnoses HBOS installation health."""
    
    def __init__(self):
        self.hbos_path = Path(__file__).parent.parent
        self.hermes_home = Path.home() / ".hermes"
        self.issues = []
        self.warnings = []
        
    def run(self):
        """Run diagnostics."""
        print("\n🏥 Hermes Business OS — Doctor\n")
        
        self._check_hermes()
        self._check_hbos_skills()
        self._check_config()
        self._check_google_workspace()
        self._check_python_deps()
        
        # Report
        print("\n" + "=" * 40)
        if not self.issues and not self.warnings:
            print("✅ All checks passed! HBOS is healthy.")
        else:
            if self.issues:
                print(f"❌ {len(self.issues)} issue(s) found:")
                for issue in self.issues:
                    print(f"   • {issue}")
            if self.warnings:
                print(f"⚠️  {len(self.warnings)} warning(s):")
                for warning in self.warnings:
                    print(f"   • {warning}")
        print("=" * 40 + "\n")
        
        return len(self.issues) == 0
    
    def _check_hermes(self):
        """Check Hermes Agent installation."""
        print("Checking Hermes Agent...")
        
        if not self.hermes_home.exists():
            self.issues.append("Hermes Agent not installed")
            return
        
        # Check hermes binary
        hermes_bin = Path.home() / ".local" / "bin" / "hermes"
        if not hermes_bin.exists():
            self.warnings.append("Hermes binary not in ~/.local/bin/hermes")
        
        # Check profiles
        profiles_dir = self.hermes_home / "profiles"
        if profiles_dir.exists():
            profiles = list(profiles_dir.iterdir())
            print(f"  ✅ Hermes installed with {len(profiles)} profile(s)")
        else:
            print(f"  ✅ Hermes installed (no profiles yet)")
    
    def _check_hbos_skills(self):
        """Check HBOS skills installation."""
        print("Checking HBOS skills...")
        
        skills_dir = self.hbos_path / "skills"
        if not skills_dir.exists():
            self.issues.append("HBOS skills directory not found")
            return
        
        skills = [d.name for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith("__")]
        print(f"  ✅ Found {len(skills)} skill(s): {', '.join(skills)}")
        
        # Check if installed in Hermes
        hermes_skills = self.hermes_home / "skills"
        if hermes_skills.exists():
            installed = [d.name for d in hermes_skills.iterdir() if d.is_dir() and d.name.startswith("hermes-")]
            if installed:
                print(f"  ✅ Installed in Hermes: {', '.join(installed)}")
            else:
                self.warnings.append("HBOS skills not installed in Hermes. Run: hbos install")
    
    def _check_config(self):
        """Check company configuration."""
        print("Checking configuration...")
        
        config_file = self.hbos_path / "config" / "empresa.yaml"
        if config_file.exists():
            print(f"  ✅ Company config found: {config_file}")
        else:
            self.warnings.append("Company config not found. Run: hbos setup")
    
    def _check_google_workspace(self):
        """Check Google Workspace integration."""
        print("Checking Google Workspace...")
        
        service_account = self.hbos_path / "config" / "google-service-account.json"
        if service_account.exists():
            print(f"  ✅ Service account found")
        else:
            print(f"  ℹ️  Service account not configured (optional)")
    
    def _check_python_deps(self):
        """Check Python dependencies."""
        print("Checking Python dependencies...")
        
        required = ["yaml", "googleapiclient", "weasyprint"]
        
        for dep in required:
            try:
                if dep == "yaml":
                    import yaml
                elif dep == "googleapiclient":
                    from googleapiclient import discovery
                elif dep == "weasyprint":
                    import weasyprint
                print(f"  ✅ {dep}")
            except ImportError:
                self.warnings.append(f"Python dependency not installed: {dep}")
