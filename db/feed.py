import feedparser
from pathlib import Path

class FeedRAG:
    def __init__(self, folder="rag/feed"):
        self.folder = Path(folder)

    def load_feeds(self):
        results = []
        for file in self.folder.glob("*.xml"):
            feed = feedparser.parse(file)
            for entry in feed.entries:
                results.append({
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "link": entry.get("link", ""),
                    "source": file.name
                })
        return results
