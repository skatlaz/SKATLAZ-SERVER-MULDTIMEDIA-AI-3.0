from __future__ import annotations
import re, json, hashlib, datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import pandas as pd

UA = "SkatlazSurfTaskMCP/1.0 (+https://skatlaz.com)"


def ensure_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def slugify_url(url: str) -> str:
    parsed = urlparse(url)
    base = (parsed.netloc + parsed.path).strip("/") or "site"
    base = re.sub(r"[^a-zA-Z0-9_-]+", "_", base)[:80]
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    return f"{base}_{h}"


def fetch_html(url: str, timeout: int = 20) -> dict:
    url = ensure_url(url)
    r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
    r.raise_for_status()
    return {"url": r.url, "status": r.status_code, "content_type": r.headers.get("content-type", ""), "html": r.text}


def extract_page_info(url: str) -> dict:
    fetched = fetch_html(url)
    html = fetched["html"]
    soup = BeautifulSoup(html, "lxml")
    title = (soup.title.string.strip() if soup.title and soup.title.string else "")
    metas = {}
    for m in soup.find_all("meta"):
        key = m.get("name") or m.get("property") or m.get("http-equiv")
        val = m.get("content")
        if key and val:
            metas[key] = val.strip()
    headings = [h.get_text(" ", strip=True) for h in soup.find_all(["h1", "h2", "h3"])][:30]
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    text = "\n".join([t for t in paragraphs if len(t) > 30])
    links = []
    for a in soup.find_all("a", href=True):
        label = a.get_text(" ", strip=True)[:120]
        href = urljoin(fetched["url"], a["href"])
        if href.startswith(("http://", "https://")):
            links.append({"label": label, "url": href})
    images = []
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if src:
            images.append({"alt": img.get("alt", ""), "url": urljoin(fetched["url"], src)})
    return {
        "url": fetched["url"], "status": fetched["status"], "title": title,
        "description": metas.get("description") or metas.get("og:description") or "",
        "metatags": metas, "headings": headings, "text": text[:20000],
        "links": links[:200], "images": images[:100],
        "created_at": datetime.datetime.now().isoformat(timespec="seconds")
    }


def simple_summary(text: str, max_sentences: int = 6) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return "Sem texto suficiente para resumo."
    sentences = re.split(r"(?<=[.!?])\s+", text)
    # score by length and keywords; simple offline summarizer
    words = re.findall(r"[a-zA-ZÀ-ÿ]{4,}", text.lower())
    stop = set("para com uma que por mais como esse essa isso este esta sobre entre pela pelo aos das dos nas nos não sim são foi ser ter cada muito também".split())
    freq = {}
    for w in words:
        if w not in stop:
            freq[w] = freq.get(w, 0) + 1
    ranked = []
    for i, s in enumerate(sentences):
        sw = re.findall(r"[a-zA-ZÀ-ÿ]{4,}", s.lower())
        score = sum(freq.get(w, 0) for w in sw) / max(1, len(sw))
        if 40 <= len(s) <= 350:
            ranked.append((score, i, s))
    top = sorted(ranked, reverse=True)[:max_sentences]
    top = sorted(top, key=lambda x: x[1])
    return " ".join(s for _, _, s in top) or text[:1200]


def analyze_url(url: str, out_dir: str | Path = "outputs") -> dict:
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    info = extract_page_info(url)
    info["summary"] = simple_summary(info.get("text", ""))
    slug = slugify_url(info["url"])
    json_path = out_dir / f"{slug}.json"
    json_path.write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")
    return {**info, "json_file": str(json_path)}


def export_results_csv(results: list[dict], path: str | Path) -> str:
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    rows = [{"url": r.get("url"), "title": r.get("title"), "description": r.get("description"), "summary": r.get("summary")} for r in results]
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")
    return str(path)
