# apps/backend/app/api/v1/skills.py
from fastapi import APIRouter, HTTPException
from app.skills.timer import TimerSkill
from app.skills.weather import WeatherSkill
from app.skills.system_time import SystemTimeSkill  # <-- add this

router = APIRouter()

@router.get("/manifests")
async def manifests():
    return [
        TimerSkill.manifest().model_dump(),
        WeatherSkill.manifest().model_dump(),
        SystemTimeSkill.manifest().model_dump(),  # <-- add this
    ]

@router.post("/run/{skill_name}")
async def run_skill(skill_name: str, params: dict):
    if skill_name == TimerSkill.name:
        return await TimerSkill().run(**params)
    if skill_name == WeatherSkill.name:
        return await WeatherSkill().run(**params)
    if skill_name == SystemTimeSkill.name:  # <-- add this
        return await SystemTimeSkill().run()
    raise HTTPException(404, f"Unknown skill {skill_name}")
