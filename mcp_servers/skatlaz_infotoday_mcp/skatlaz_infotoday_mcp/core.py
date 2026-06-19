from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import feedparser
import requests
from bs4 import BeautifulSoup

USER_AGENT = "SkatlazInfoTodayMCP/1.0 (contact: skatlaz.com)"


class MCPError(Exception):
    pass


@dataclass
class InfoTodayConfig:
    data_dir: Path = Path("data")
    timeout: int = 20


class JsonStore:
    def __init__(self, path: Path, default: Any):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.write(default)

    def read(self) -> Any:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def write(self, data: Any) -> None:
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


class SkatlazInfoTodayMCP:
    def __init__(self, data_dir: str | Path = "data"):
        self.config = InfoTodayConfig(data_dir=Path(data_dir))
        self.config.data_dir.mkdir(parents=True, exist_ok=True)
        self.yellow_store = JsonStore(self.config.data_dir / "yellow_pages.json", [])
        self.contacts_store = JsonStore(self.config.data_dir / "contacts.json", [])

    def _get(self, url: str, params: Optional[dict] = None) -> requests.Response:
        r = requests.get(url, params=params, timeout=self.config.timeout, headers={"User-Agent": USER_AGENT})
        r.raise_for_status()
        return r

    # ---------------- Research ----------------
    def wikipedia_summary(self, query: str, lang: str = "pt") -> Dict[str, Any]:
        title = query.strip().replace(" ", "_")
        url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"
        try:
            data = self._get(url).json()
            return {
                "title": data.get("title", query),
                "summary": data.get("extract", ""),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
                "source": "Wikipedia",
            }
        except Exception as e:
            return {"title": query, "summary": "", "error": str(e), "source": "Wikipedia"}

    def arxiv_search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        url = "http://export.arxiv.org/api/query"
        try:
            text = self._get(url, params=params).text
            feed = feedparser.parse(text)
            results = []
            for entry in feed.entries:
                results.append({
                    "title": entry.get("title", "").replace("\n", " ").strip(),
                    "summary": entry.get("summary", "").replace("\n", " ").strip(),
                    "url": entry.get("link"),
                    "published": entry.get("published"),
                    "authors": [a.get("name") for a in entry.get("authors", [])],
                    "source": "arXiv",
                })
            return results
        except Exception as e:
            return [{"error": str(e), "source": "arXiv"}]

    def web_read(self, url: str, max_chars: int = 5000) -> Dict[str, Any]:
        try:
            html = self._get(url).text
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()
            title = soup.title.string.strip() if soup.title and soup.title.string else url
            text = "\n".join(line.strip() for line in soup.get_text("\n").splitlines() if line.strip())
            return {"title": title, "url": url, "text": text[:max_chars], "source": "web"}
        except Exception as e:
            return {"url": url, "text": "", "error": str(e), "source": "web"}

    def simple_summary(self, text: str, max_sentences: int = 5) -> str:
        clean = re.sub(r"\s+", " ", text).strip()
        sentences = re.split(r"(?<=[.!?])\s+", clean)
        return " ".join(sentences[:max_sentences])

    # ---------------- Weather ----------------
    def geocode(self, address: str) -> Optional[Dict[str, Any]]:
        params = {"q": address, "format": "json", "limit": 1, "addressdetails": 1}
        try:
            data = self._get("https://nominatim.openstreetmap.org/search", params=params).json()
            if not data:
                return None
            item = data[0]
            return {
                "lat": float(item["lat"]),
                "lon": float(item["lon"]),
                "display_name": item.get("display_name"),
                "address": item.get("address", {}),
                "source": "OpenStreetMap/Nominatim",
            }
        except Exception as e:
            return {"error": str(e), "source": "OpenStreetMap/Nominatim"}

    def reverse_geocode(self, lat: float, lon: float) -> Dict[str, Any]:
        params = {"lat": lat, "lon": lon, "format": "json", "addressdetails": 1}
        try:
            data = self._get("https://nominatim.openstreetmap.org/reverse", params=params).json()
            return {"display_name": data.get("display_name"), "address": data.get("address", {}), "source": "OpenStreetMap/Nominatim"}
        except Exception as e:
            return {"error": str(e), "source": "OpenStreetMap/Nominatim"}

    def weather_current(self, city: str) -> Dict[str, Any]:
        geo = self.geocode(city)
        if not geo or geo.get("error"):
            return {"error": "cidade não encontrada", "geo": geo}
        params = {
            "latitude": geo["lat"],
            "longitude": geo["lon"],
            "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code",
            "timezone": "auto",
        }
        try:
            data = self._get("https://api.open-meteo.com/v1/forecast", params=params).json()
            return {"city": city, "geo": geo, "current": data.get("current", {}), "units": data.get("current_units", {}), "source": "Open-Meteo"}
        except Exception as e:
            return {"error": str(e), "source": "Open-Meteo"}

    def weather_forecast(self, city: str, days: int = 7) -> Dict[str, Any]:
        geo = self.geocode(city)
        if not geo or geo.get("error"):
            return {"error": "cidade não encontrada", "geo": geo}
        params = {
            "latitude": geo["lat"],
            "longitude": geo["lon"],
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
            "forecast_days": min(max(days, 1), 16),
            "timezone": "auto",
        }
        try:
            data = self._get("https://api.open-meteo.com/v1/forecast", params=params).json()
            return {"city": city, "geo": geo, "daily": data.get("daily", {}), "units": data.get("daily_units", {}), "source": "Open-Meteo"}
        except Exception as e:
            return {"error": str(e), "source": "Open-Meteo"}

    # ---------------- Maps / Transport ----------------
    def route_osrm(self, origin: str, destination: str, profile: str = "driving") -> Dict[str, Any]:
        start = self.geocode(origin)
        end = self.geocode(destination)
        if not start or not end or start.get("error") or end.get("error"):
            return {"error": "não foi possível geocodificar origem/destino", "origin": start, "destination": end}
        url = f"https://router.project-osrm.org/route/v1/{profile}/{start['lon']},{start['lat']};{end['lon']},{end['lat']}"
        params = {"overview": "full", "geometries": "geojson", "steps": "true"}
        try:
            data = self._get(url, params=params).json()
            if data.get("code") != "Ok":
                return {"error": data.get("message", "rota não encontrada"), "source": "OSRM"}
            r = data["routes"][0]
            steps = []
            for leg in r.get("legs", []):
                for step in leg.get("steps", [])[:20]:
                    maneuver = step.get("maneuver", {})
                    steps.append({
                        "name": step.get("name"),
                        "distance_m": step.get("distance"),
                        "duration_s": step.get("duration"),
                        "type": maneuver.get("type"),
                        "modifier": maneuver.get("modifier"),
                    })
            return {
                "origin": start,
                "destination": end,
                "distance_km": round(r.get("distance", 0) / 1000, 2),
                "duration_min": round(r.get("duration", 0) / 60, 1),
                "steps": steps,
                "source": "OSRM/OpenStreetMap",
            }
        except Exception as e:
            return {"error": str(e), "source": "OSRM/OpenStreetMap"}

    def nearby_osm(self, category: str, city: str, radius_m: int = 3000, limit: int = 20) -> List[Dict[str, Any]]:
        geo = self.geocode(city)
        if not geo or geo.get("error"):
            return [{"error": "local não encontrado", "geo": geo}]
        q = self._overpass_query(category, geo["lat"], geo["lon"], radius_m)
        try:
            data = self._get("https://overpass-api.de/api/interpreter", params={"data": q}).json()
            out = []
            for el in data.get("elements", [])[:limit]:
                tags = el.get("tags", {})
                out.append({
                    "name": tags.get("name", "Sem nome"),
                    "category": category,
                    "lat": el.get("lat") or el.get("center", {}).get("lat"),
                    "lon": el.get("lon") or el.get("center", {}).get("lon"),
                    "phone": tags.get("phone") or tags.get("contact:phone"),
                    "website": tags.get("website") or tags.get("contact:website"),
                    "opening_hours": tags.get("opening_hours"),
                    "source": "OpenStreetMap/Overpass",
                })
            return out
        except Exception as e:
            return [{"error": str(e), "source": "OpenStreetMap/Overpass"}]

    def _overpass_query(self, category: str, lat: float, lon: float, radius_m: int) -> str:
        c = category.lower()
        tags = []
        if any(x in c for x in ["oficina", "mecanica", "mecânica", "carro"]):
            tags.append('["shop"="car_repair"]')
            tags.append('["amenity"="vehicle_inspection"]')
        elif "farm" in c:
            tags.append('["amenity"="pharmacy"]')
        elif "hospital" in c:
            tags.append('["amenity"="hospital"]')
        elif "restaurante" in c or "restaurant" in c:
            tags.append('["amenity"="restaurant"]')
        elif "posto" in c or "combust" in c:
            tags.append('["amenity"="fuel"]')
        else:
            tags.append(f'["name"~"{category}",i]')
        blocks = []
        for t in tags:
            blocks.append(f"node{t}(around:{radius_m},{lat},{lon});way{t}(around:{radius_m},{lat},{lon});relation{t}(around:{radius_m},{lat},{lon});")
        return f"[out:json][timeout:25];({''.join(blocks)});out center tags;"

    def transport_plan_simple(self, origin: str, destination: str) -> Dict[str, Any]:
        # Base open-source mínima: caminhada/carro com OSM + nota GTFS/OTP para produção.
        route = self.route_osrm(origin, destination, profile="driving")
        route["transport_note"] = "Para ônibus/metrô/trem real, conecte um feed GTFS local ou OpenTripPlanner. Este MCP já deixa o ponto de integração preparado."
        return route

    # ---------------- Yellow Pages / Contacts ----------------
    def yellow_import_csv(self, csv_path: str) -> Dict[str, Any]:
        data = self.yellow_store.read()
        count = 0
        with open(csv_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                data.append(dict(row))
                count += 1
        self.yellow_store.write(data)
        return {"imported": count, "total": len(data)}

    def yellow_add(self, item: Dict[str, Any]) -> Dict[str, Any]:
        data = self.yellow_store.read()
        data.append(item)
        self.yellow_store.write(data)
        return {"added": item, "total": len(data)}

    def yellow_search(self, query: str = "", city: str = "", district: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        data = self.yellow_store.read()
        q = query.lower().strip()
        c = city.lower().strip()
        d = district.lower().strip()
        results = []
        for item in data:
            hay = " ".join(str(item.get(k, "")) for k in ["name", "category", "services", "address", "district", "city"]).lower()
            if q and q not in hay:
                continue
            if c and c not in str(item.get("city", "")).lower():
                continue
            if d and d not in str(item.get("district", "")).lower():
                continue
            results.append(item)
        return sorted(results, key=lambda x: float(x.get("rating", 0) or 0), reverse=True)[:limit]

    def contacts_add(self, contact: Dict[str, Any]) -> Dict[str, Any]:
        data = self.contacts_store.read()
        data.append(contact)
        self.contacts_store.write(data)
        return {"added": contact, "total": len(data)}

    def contacts_search(self, query: str) -> List[Dict[str, Any]]:
        data = self.contacts_store.read()
        q = query.lower()
        return [x for x in data if q in json.dumps(x, ensure_ascii=False).lower()]

    # ---------------- Prompt Router ----------------
    def ask(self, prompt: str) -> Dict[str, Any]:
        p = prompt.lower()
        if any(w in p for w in ["clima", "tempo", "meteorologia", "previsão", "previsao"]):
            city = self._extract_after(prompt, ["em", "de", "para"]) or "São Paulo"
            return {"tool": "weather_current", "result": self.weather_current(city)}
        if any(w in p for w in ["rota", "trajeto", "como ir", "itinerário", "itinerario"]):
            parts = re.split(r"\s+para\s+|\s+até\s+|\s+ate\s+", prompt, flags=re.I)
            if len(parts) >= 2:
                origin = re.sub(r".*?(de|da|do)\s+", "", parts[0], flags=re.I).strip()
                dest = parts[1].strip()
                return {"tool": "route_osrm", "result": self.route_osrm(origin, dest)}
        if any(w in p for w in ["oficina", "farmacia", "farmácia", "restaurante", "hospital", "posto"]):
            city = "São Paulo"
            local_results = self.yellow_search(query=prompt, city=city)
            osm_results = self.nearby_osm(prompt, city) if len(local_results) < 3 else []
            return {"tool": "yellow_pages+osm", "local": local_results, "osm": osm_results}
        if any(w in p for w in ["wikipedia", "pesquise", "resuma", "artigo"]):
            q = prompt.replace("pesquise", "").replace("wikipedia", "").strip()
            return {"tool": "wikipedia_summary", "result": self.wikipedia_summary(q)}
        return {"tool": "none", "message": "Não entendi a intenção. Use clima, rota, oficina/farmácia/restaurante/hospital, ou pesquise."}

    def _extract_after(self, text: str, keys: List[str]) -> Optional[str]:
        for k in keys:
            m = re.search(rf"\b{k}\b\s+(.+)$", text, flags=re.I)
            if m:
                return m.group(1).strip()
        return None
