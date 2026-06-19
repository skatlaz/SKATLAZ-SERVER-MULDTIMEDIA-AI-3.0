from pathlib import Path
from .config import RAG_DIR

class SimpleRAG:
    def __init__(self, base_dir: Path | None = None):
        self.base_dir = base_dir or RAG_DIR

    def list_docs(self):
        return [str(p.relative_to(self.base_dir)) for p in self.base_dir.rglob('*.md')]

    def search(self, query: str, limit=5):
        q=query.lower(); results=[]
        for p in self.base_dir.rglob('*.md'):
            text=p.read_text(encoding='utf-8', errors='ignore')
            score=sum(1 for word in q.split() if word in text.lower())
            if score:
                idx=text.lower().find(q.split()[0]) if q.split() else 0
                results.append({'file':str(p.relative_to(self.base_dir)),'score':score,'snippet':text[max(0,idx-120):idx+500]})
        return sorted(results,key=lambda x:x['score'], reverse=True)[:limit]
