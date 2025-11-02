# apps/backend/app/skills/system_exec.py
import subprocess
import sys
from .base import Skill, ToolSpec

class OpenApplicationSkill(Skill):
    """Opens a native application on the user's computer."""
    name = "system.open_app"

    @classmethod
    def manifest(cls) -> ToolSpec:
        # This tells the LLM what parameters this skill needs
        return ToolSpec(
            name=cls.name,
            description=cls.__doc__ or "",
            parameters={
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "The name of the application to open (e.g., 'notepad', 'calculator', 'Google Chrome')."
                    }
                },
                "required": ["app_name"]
            }
        )

    async def run(self, app_name: str):
        try:
            # --- This is the OS-specific part ---
            if sys.platform == "win32":
                # Example for Windows. 'start' is a shell command.
                if app_name.lower() == 'notepad':
                    subprocess.Popen(["notepad.exe"])
                elif app_name.lower() == 'calculator':
                    subprocess.Popen(["calc.exe"])
                else:
                    # Generic 'start' command for other apps
                    subprocess.Popen(["start", app_name], shell=True)
                
            elif sys.platform == "darwin":
                # Example for macOS
                subprocess.Popen(["open", "-a", app_name])
                
            else:
                # Example for Linux
                subprocess.Popen([app_name.lower()])
            # -------------------------------------
                
            return {"spoken": f"Opening {app_name}."}
        
        except Exception as e:
            return {"spoken": f"Sorry, I couldn't open {app_name}: {str(e)}"}