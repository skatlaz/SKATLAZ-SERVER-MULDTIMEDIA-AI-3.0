import math
from collections import Counter
from typing import Iterable, List, Tuple

def chunk_text(text: str, size: int=1200, overlap: int=160) -> list[str]:
    clean=" ".join((text or "").split())
    chunks=[]; start=0
    while start < len(clean):
        chunks.append(clean[start:start+size]); start += max(1, size-overlap)
    return chunks

def _tokens(text: str) -> Counter:
    return Counter(w.lower().strip(".,;:!?()[]{}\"'") for w in text.split() if len(w.strip())>2)

def cosine_bow(a: str, b: str) -> float:
    ca,cb=_tokens(a),_tokens(b)
    if not ca or not cb: return 0.0
    keys=set(ca)|set(cb)
    dot=sum(ca[k]*cb[k] for k in keys)
    na=math.sqrt(sum(v*v for v in ca.values())); nb=math.sqrt(sum(v*v for v in cb.values()))
    return dot/(na*nb) if na and nb else 0.0

def search_chunks(query: str, chunks: Iterable, limit: int=6) -> List[Tuple[float, object]]:
    scored=[(cosine_bow(query, c.text), c) for c in chunks]
    return sorted(scored, key=lambda x:x[0], reverse=True)[:limit]
