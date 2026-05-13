"""
Hermes Business OS - Skill Engine
Manages skill registration, discovery, and execution
"""
import os
import importlib
import inspect
from typing import Dict, Any, List, Optional
from pathlib import Path

from app.skills.base import BaseSkill
from core.config import client_config


class SkillEngine:
    """Central engine for skill management."""
    
    def __init__(self):
        self._skills: Dict[str, BaseSkill] = {}
        self._discover_skills()
    
    def _discover_skills(self):
        """Auto-discover skills from skills/ directory."""
        # Get the directory where skills are located
        backend_dir = Path(__file__).parent.parent.parent  # backend/
        skills_dir = backend_dir / "app" / "skills"
        
        print(f"🔍 Discovering skills in: {skills_dir}")
        
        if not skills_dir.exists():
            print(f"⚠️  Skills directory not found: {skills_dir}")
            return
        
        # Look for skill modules
        for item in skills_dir.iterdir():
            if item.is_dir() and not item.name.startswith("__"):
                self._load_skill_module(item.name)
    
    def _load_skill_module(self, module_name: str):
        """Load a skill module and register its skills."""
        try:
            # Try loading from skill.py inside the module directory
            skill_module = importlib.import_module(f"app.skills.{module_name}.skill")
            
            # Find all BaseSkill subclasses
            for name, obj in inspect.getmembers(skill_module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, BaseSkill) and 
                    obj is not BaseSkill and
                    hasattr(obj, 'name')):
                    
                    skill_instance = obj()
                    self._skills[skill_instance.name] = skill_instance
                    print(f"✅ Skill loaded: {skill_instance.name} v{skill_instance.version}")
                    
        except Exception as e:
            print(f"⚠️  Failed to load skill module '{module_name}': {e}")
    
    def list_skills(self) -> List[Dict[str, str]]:
        """List all registered skills."""
        return [
            {
                "name": name,
                "description": skill.description,
                "version": skill.version,
                "actions": len(skill.actions)
            }
            for name, skill in self._skills.items()
        ]
    
    def get_skill(self, name: str) -> Optional[BaseSkill]:
        """Get a skill by name."""
        return self._skills.get(name)
    
    def execute(self, skill_name: str, action: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute an action on a skill."""
        skill = self.get_skill(skill_name)
        
        if not skill:
            return {
                "success": False,
                "error": f"Skill '{skill_name}' not found",
                "available_skills": list(self._skills.keys())
            }
        
        return skill.execute(action, parameters)
    
    def execute_by_intent(self, intent: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute based on natural language intent (simple keyword matching)."""
        parameters = parameters or {}
        intent_lower = intent.lower()
        
        # Simple routing logic - can be enhanced with NLP
        for skill_name, skill in self._skills.items():
            for action_name in skill.actions.keys():
                if action_name.lower() in intent_lower or skill_name.lower() in intent_lower:
                    return self.execute(skill_name, action_name, parameters)
        
        return {
            "success": False,
            "error": f"No skill found for intent: '{intent}'",
            "hint": "Try specifying skill and action explicitly"
        }
