import requests
from .config import DATA_DIR, USER_AGENT
from .utils import load_json, filter_local

MB = "https://musicbrainz.org/ws/2"


def musicbrainz_artist(query: str):
    r = requests.get(f"{MB}/artist", params={"query": query, "fmt":"json", "limit":10}, headers={"User-Agent": USER_AGENT}, timeout=20)
    r.raise_for_status()
    return [{"name": a.get("name"), "type": a.get("type"), "country": a.get("country"), "score": a.get("score"), "id": a.get("id"), "source":"MusicBrainz"} for a in r.json().get("artists", [])]


def search_local_music(query: str = "", genre: str = ""):
    return filter_local(load_json(DATA_DIR / "music.json"), query, genre)


def smart_playlist(mood: str = "", genre: str = ""):
    playlists = load_json(DATA_DIR / "playlists.json")
    result = []
    for p in playlists:
        blob = str(p).lower()
        if (not mood or mood.lower() in blob) and (not genre or genre.lower() in blob):
            result.append(p)
    return result


def arrangement_suggestions(style: str):
    base = search_local_music(style, "")
    if base:
        return base[0].get("suggestions", [])
    return ["piano leve", "baixo orgânico", "bateria suave", "guitarra estéreo", "pad atmosférico"]
