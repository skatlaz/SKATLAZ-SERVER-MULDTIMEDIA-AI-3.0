import json, csv
from pathlib import Path

class LocalSportsDB:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)

    def _load(self, name):
        path = self.data_dir / name
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    def search(self, q):
        q = (q or "").lower()
        results = []
        for file_name, kind in [
            ("teams.json", "team"),
            ("athletes.json", "athlete"),
            ("competitions.json", "competition"),
            ("worldcup_history.json", "worldcup"),
            ("olympics_history.json", "olympics"),
        ]:
            for item in self._load(file_name):
                blob = json.dumps(item, ensure_ascii=False).lower()
                if q in blob:
                    row = dict(item)
                    row["_kind"] = kind
                    results.append(row)
        return results

    def list_worldcups(self):
        return self._load("worldcup_history.json")

    def list_olympics(self):
        return self._load("olympics_history.json")

    def list_competitions(self):
        return self._load("competitions.json")

    def export_csv(self, rows, output_path):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if not rows:
            output_path.write_text("", encoding="utf-8")
            return str(output_path)
        keys = sorted(set().union(*(r.keys() for r in rows)))
        with output_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)
        return str(output_path)
