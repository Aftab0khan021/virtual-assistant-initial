import asyncio
from .base import Skill

class TimerSkill(Skill):
    """Set a countdown timer and notify when it ends."""
    name = "timer.set"

    async def run(self, seconds: int):
        await asyncio.sleep(int(seconds))
        return {"spoken": f"Timer done after {seconds} seconds"}
