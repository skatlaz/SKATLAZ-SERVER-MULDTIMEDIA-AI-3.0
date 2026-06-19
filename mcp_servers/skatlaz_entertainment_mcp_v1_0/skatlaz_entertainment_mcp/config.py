import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "").strip()
USER_AGENT = os.getenv("SKATLAZ_USER_AGENT", "SkatlazEntertainmentMCP/1.0 (skatlaz.com)")
