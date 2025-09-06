# apps/backend/app/skills/system_time.py
from .base import Skill
from datetime import datetime

class SystemTimeSkill(Skill):
    """Tell the current time (system clock)."""
    name = "system.time"

    async def run(self):
        now = datetime.now().strftime("%I:%M %p")
        return {"spoken": f"It's {now}."}
