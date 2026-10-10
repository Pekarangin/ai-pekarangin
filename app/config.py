import os
from pathlib import Path
from dotenv import load_dotenv

# Muat file .env jika ada
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "Pekarang.in AI Engine"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")

    # Gemini API
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    _raw_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    GEMINI_MODEL: str = "gemini-2.5-flash" if (not _raw_model or _raw_model == "gemini-1.5-flash") else _raw_model

    # Backend Express Integration
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:3000")

    @property
    def has_gemini_key(self) -> bool:
        return bool(self.GEMINI_API_KEY and self.GEMINI_API_KEY != "your_gemini_api_key_here")

settings = Settings()
