import json
from pathlib import Path

class JSONLoader:
    def load(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
