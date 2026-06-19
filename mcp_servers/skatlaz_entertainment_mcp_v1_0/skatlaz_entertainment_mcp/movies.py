import requests
from .config import DATA_DIR, TMDB_API_KEY
from .utils import load_json, filter_local, simple_summary

TVMAZE = "https://api.tvmaze.com"
TMDB = "https://api.themoviedb.org/3"


def search_local_movies(query: str = "", genre: str = ""):
    return filter_local(load_json(DATA_DIR / "movies.json"), query, genre)


def tvmaze_search_show(query: str):
    r = requests.get(f"{TVMAZE}/search/shows", params={"q": query}, timeout=20)
    r.raise_for_status()
    data = r.json()
    results = []
    for row in data[:10]:
        s = row.get("show", {})
        results.append({
            "id": s.get("id"), "name": s.get("name"), "type": s.get("type"),
            "language": s.get("language"), "genres": s.get("genres", []),
            "rating": (s.get("rating") or {}).get("average"),
            "summary": simple_summary((s.get("summary") or "").replace("<p>", "").replace("</p>", "")),
            "officialSite": s.get("officialSite"), "source": "TVMaze"
        })
    return results


def tvmaze_episodes(show_id: int):
    r = requests.get(f"{TVMAZE}/shows/{show_id}/episodes", timeout=20)
    r.raise_for_status()
    return [{"season": e.get("season"), "number": e.get("number"), "name": e.get("name"), "airdate": e.get("airdate"), "summary": simple_summary((e.get("summary") or "").replace("<p>", "").replace("</p>", ""), 2)} for e in r.json()]


def tmdb_search_movie(query: str):
    if not TMDB_API_KEY:
        return {"error":"TMDB_API_KEY não configurada. Use TVMaze/local ou configure .env."}
    r = requests.get(f"{TMDB}/search/movie", params={"api_key": TMDB_API_KEY, "query": query, "language":"pt-BR"}, timeout=20)
    r.raise_for_status()
    return r.json().get("results", [])[:10]


def recommend_movies(genre: str = "", query: str = ""):
    local = search_local_movies(query, genre)
    return local[:10]
