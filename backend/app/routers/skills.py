"""
Skills management and execution endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from core.config import client_config
from app.skills.engine import SkillEngine

router = APIRouter()
skill_engine = SkillEngine()


class SkillExecute(BaseModel):
    skill: str
    action: str
    parameters: Dict[str, Any] = {}


@router.get("/skills")
async def list_skills():
    """List all available skills."""
    return {
        "skills": skill_engine.list_skills(),
        "departments": [
            {
                "name": d.get("name"),
                "enabled": d.get("enabled"),
                "skills": d.get("skills", [])
            }
            for d in client_config.departments
        ]
    }


@router.post("/skills/execute")
async def execute_skill(request: SkillExecute):
    """Execute a skill action."""
    result = skill_engine.execute(
        skill_name=request.skill,
        action=request.action,
        parameters=request.parameters
    )
    return result


@router.get("/skills/{skill_name}/actions")
async def get_skill_actions(skill_name: str):
    """Get available actions for a skill."""
    skill = skill_engine.get_skill(skill_name)
    if not skill:
        raise HTTPException(status_code=404, detail=f"Skill '{skill_name}' not found")
    return {
        "skill": skill_name,
        "actions": skill.list_actions()
    }
