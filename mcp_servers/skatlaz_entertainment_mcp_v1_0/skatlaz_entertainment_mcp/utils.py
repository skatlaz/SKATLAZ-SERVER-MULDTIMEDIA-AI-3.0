import json, csv, re
from pathlib import Path
from typing import Any, Iterable


def load_json(path: Path, default=None):
    if default is None: default = []
    if not path.exists(): return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def save_json(path: Path, data: Any):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def simple_summary(text: str, max_sentences: int = 4) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if not text: return ""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return " ".join(sentences[:max_sentences])


def score_match(item: dict, query: str) -> int:
    q = (query or "").lower()
    blob = json.dumps(item, ensure_ascii=False).lower()
    score = 0
    for token in re.findall(r"\w+", q):
        if token in blob: score += 1
    return score


def filter_local(items: Iterable[dict], query: str = "", genre: str = ""):
    rows = list(items)
    if query:
        rows = sorted([r for r in rows if score_match(r, query) > 0], key=lambda r: score_match(r, query), reverse=True)
    if genre:
        g = genre.lower()
        rows = [r for r in rows if g in json.dumps(r.get("genres", r.get("genre", "")), ensure_ascii=False).lower()]
    return rows
