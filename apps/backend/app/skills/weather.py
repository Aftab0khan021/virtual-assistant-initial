from .base import Skill
import httpx

class WeatherSkill(Skill):
    """Fetch current weather for given coordinates using Open-Meteo."""
    name = "weather.get"

    async def run(self, latitude: float, longitude: float):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {"latitude": latitude, "longitude": longitude, "current_weather": True}
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            data = r.json()
        cw = data.get("current_weather", {})
        temp = cw.get("temperature")
        wind = cw.get("windspeed")
        return {
            "spoken": f"Current temperature is {temp}°C with wind {wind} km/h.",
            "data": cw,
        }
