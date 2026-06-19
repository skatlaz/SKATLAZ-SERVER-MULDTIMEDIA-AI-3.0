import feedparser
from datetime import datetime

def read_rss(url, limit=10):
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries[:limit]:
        items.append({
            "title": entry.get("title"),
            "link": entry.get("link"),
            "summary": entry.get("summary", ""),
            "published": entry.get("published", ""),
            "source": feed.feed.get("title", url),
            "fetched_at": datetime.utcnow().isoformat() + "Z"
        })
    return {"feed": feed.feed.get("title", url), "items": items}
