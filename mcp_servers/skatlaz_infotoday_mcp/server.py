from typing import Any, Dict

from fastapi import FastAPI
from pydantic import BaseModel

from skatlaz_infotoday_mcp.core import SkatlazInfoTodayMCP

app = FastAPI(title="Skatlaz InfoToday MCP", version="1.0")
mcp = SkatlazInfoTodayMCP("data")

class PromptRequest(BaseModel):
    prompt: str

class WeatherRequest(BaseModel):
    city: str
    days: int = 7

class RouteRequest(BaseModel):
    origin: str
    destination: str
    profile: str = "driving"

class YellowAddRequest(BaseModel):
    item: Dict[str, Any]

class YellowSearchRequest(BaseModel):
    query: str = ""
    city: str = ""
    district: str = ""
    limit: int = 20

class ResearchRequest(BaseModel):
    query: str
    lang: str = "pt"
    max_results: int = 5

@app.get("/")
def root():
    return {"name": "Skatlaz InfoToday MCP", "status": "ok", "docs": "/docs"}

@app.post("/mcp/ask")
def ask(req: PromptRequest):
    return mcp.ask(req.prompt)

@app.post("/mcp/research/wikipedia")
def wikipedia(req: ResearchRequest):
    return mcp.wikipedia_summary(req.query, req.lang)

@app.post("/mcp/research/arxiv")
def arxiv(req: ResearchRequest):
    return mcp.arxiv_search(req.query, req.max_results)

@app.post("/mcp/weather/current")
def weather_current(req: WeatherRequest):
    return mcp.weather_current(req.city)

@app.post("/mcp/weather/forecast")
def weather_forecast(req: WeatherRequest):
    return mcp.weather_forecast(req.city, req.days)

@app.post("/mcp/maps/geocode")
def geocode(req: ResearchRequest):
    return mcp.geocode(req.query)

@app.post("/mcp/maps/route")
def route(req: RouteRequest):
    return mcp.route_osrm(req.origin, req.destination, req.profile)

@app.post("/mcp/transport/plan")
def transport_plan(req: RouteRequest):
    return mcp.transport_plan_simple(req.origin, req.destination)

@app.post("/mcp/yellow/add")
def yellow_add(req: YellowAddRequest):
    return mcp.yellow_add(req.item)

@app.post("/mcp/yellow/search")
def yellow_search(req: YellowSearchRequest):
    return mcp.yellow_search(req.query, req.city, req.district, req.limit)

@app.post("/mcp/nearby/search")
def nearby(req: YellowSearchRequest):
    city = req.city or "São Paulo"
    return mcp.nearby_osm(req.query, city, limit=req.limit)
