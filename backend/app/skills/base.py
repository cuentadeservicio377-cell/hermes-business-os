"""
Hermes Business OS - Base Skill
All skills must inherit from this class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class BaseSkill(ABC):
    """Base class for all department skills."""
    
    name: str = "base"
    description: str = "Base skill"
    version: str = "1.0.0"
    
    def __init__(self):
        self.actions = self._register_actions()
    
    @abstractmethod
    def _register_actions(self) -> Dict[str, callable]:
        """Register available actions. Must be implemented by subclasses."""
        return {}
    
    def list_actions(self) -> List[Dict[str, str]]:
        """List all available actions with descriptions."""
        return [
            {"name": name, "description": getattr(func, "__doc__", "No description")}
            for name, func in self.actions.items()
        ]
    
    def execute(self, action: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute an action by name."""
        parameters = parameters or {}
        
        if action not in self.actions:
            return {
                "success": False,
                "error": f"Action '{action}' not found in skill '{self.name}'",
                "available_actions": list(self.actions.keys())
            }
        
        try:
            result = self.actions[action](**parameters)
            return {
                "success": True,
                "skill": self.name,
                "action": action,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "skill": self.name,
                "action": action,
                "error": str(e)
            }


def action(description: str = ""):
    """Decorator to mark methods as actions with descriptions."""
    def decorator(func):
        func.__doc__ = description or func.__doc__
        return func
    return decorator
