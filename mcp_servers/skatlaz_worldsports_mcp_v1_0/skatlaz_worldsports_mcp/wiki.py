import requests

UA = {"User-Agent": "SkatlazWorldSportsMCP/1.0 (research; contact: skatlaz.com)"}

def wikipedia_summary(query, lang="en"):
    # First search a page title, then summary.
    search_url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {"action":"query","list":"search","srsearch":query,"format":"json","utf8":1}
    r = requests.get(search_url, params=params, headers=UA, timeout=20)
    r.raise_for_status()
    results = r.json().get("query", {}).get("search", [])
    if not results:
        return {"query": query, "found": False}
    title = results[0]["title"]
    summary_url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title.replace(' ', '_')}"
    s = requests.get(summary_url, headers=UA, timeout=20)
    s.raise_for_status()
    data = s.json()
    return {
        "query": query,
        "found": True,
        "title": data.get("title"),
        "extract": data.get("extract"),
        "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
        "thumbnail": data.get("thumbnail", {}).get("source")
    }

def wikidata_search(query, limit=5):
    url = "https://www.wikidata.org/w/api.php"
    params = {"action":"wbsearchentities","search":query,"language":"en","format":"json","limit":limit}
    r = requests.get(url, params=params, headers=UA, timeout=20)
    r.raise_for_status()
    return r.json().get("search", [])
