from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None
    MODEL_PROVIDER: str = "openai"
    DATABASE_URL: str = "sqlite+aiosqlite:///./assistant.db"
    REDIS_URL: str | None = None
    STT_ENGINE: str = "whispercpp"  # or "vosk"
    TTS_ENGINE: str = "pyttsx3"      # or "edge-tts"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
