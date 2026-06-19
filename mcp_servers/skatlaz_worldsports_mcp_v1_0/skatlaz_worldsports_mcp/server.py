from fastapi import FastAPI, Query
from pydantic import BaseModel
from .localdb import LocalSportsDB
from .wiki import wikipedia_summary, wikidata_search
from .rss import read_rss
from .apis import TheSportsDB, FootballData
from .reports import markdown_report
from pathlib import Path

app = FastAPI(title="Skatlaz WorldSports MCP", version="1.0.0")
db = LocalSportsDB("data")

class SearchRequest(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"ok": True, "mcp": "skatlaz_worldsports_mcp", "version": "1.0.0"}

@app.get("/sports/local/search")
def local_search(q: str):
    return {"query": q, "results": db.search(q)}

@app.get("/sports/worldcup/history")
def worldcup_history():
    return {"results": db.list_worldcups()}

@app.get("/sports/olympics/history")
def olympics_history():
    return {"results": db.list_olympics()}

@app.get("/sports/competitions")
def competitions():
    return {"results": db.list_competitions()}

@app.get("/sports/wiki/summary")
def wiki_summary(query: str, lang: str = "en"):
    return wikipedia_summary(query, lang=lang)

@app.get("/sports/wikidata/search")
def wikidata(query: str, limit: int = 5):
    return {"query": query, "results": wikidata_search(query, limit=limit)}

@app.get("/sports/rss")
def sports_rss(url: str, limit: int = 10):
    return read_rss(url, limit=limit)

@app.get("/sports/thesportsdb/team")
def thesportsdb_team(name: str):
    return {"query": name, "results": TheSportsDB().search_team(name)}

@app.get("/sports/thesportsdb/player")
def thesportsdb_player(name: str):
    return {"query": name, "results": TheSportsDB().search_player(name)}

@app.get("/sports/football-data/competitions")
def football_data_competitions():
    return FootballData().competitions()

@app.get("/sports/football-data/standings")
def football_data_standings(code: str = "PL"):
    return FootballData().standings(code)

@app.get("/sports/report/worldcup")
def report_worldcup():
    out = markdown_report(
        "World Cup History Report",
        [("History", db.list_worldcups()), ("Local Search Brazil", db.search("Brazil"))],
        "reports/worldcup_report.md"
    )
    return {"report": out}

@app.get("/sports/export/search_csv")
def export_search_csv(q: str):
    rows = db.search(q)
    out = db.export_csv(rows, f"reports/search_{q.replace(' ','_')}.csv")
    return {"file": out, "rows": len(rows)}
