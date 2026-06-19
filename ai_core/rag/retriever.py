from ai_core.models import RAGCollection, DocumentSource, RAGChunk
from .vector_store import chunk_text, search_chunks

def extract_text_from_source(source: DocumentSource) -> str:
    if source.raw_text: return source.raw_text
    if source.file:
        path=source.file.path; lower=path.lower()
        if lower.endswith((".txt",".md",".csv",".html",".json")):
            return open(path, "r", encoding="utf-8", errors="ignore").read()
        if lower.endswith(".pdf"):
            try:
                from pypdf import PdfReader
                return "\n".join(page.extract_text() or "" for page in PdfReader(path).pages)
            except Exception as exc: return f"[PDF extraction failed: {exc}]"
        if lower.endswith(".docx"):
            try:
                import docx
                d=docx.Document(path)
                return "\n".join(p.text for p in d.paragraphs)
            except Exception as exc: return f"[DOCX extraction failed: {exc}]"
    return ""

def index_source(source: DocumentSource, chunk_size: int=1200) -> int:
    text=extract_text_from_source(source)
    RAGChunk.objects.filter(source=source).delete()
    count=0
    for i, chunk in enumerate(chunk_text(text, size=chunk_size)):
        RAGChunk.objects.create(collection=source.collection, source=source, text=chunk, metadata={"chunk": i})
        count += 1
    source.indexed=True; source.save(update_fields=["indexed", "updated_at"])
    return count

def retrieve_context(collection: RAGCollection|None, query: str, limit: int=6) -> str:
    if not collection: return ""
    matches=search_chunks(query, collection.chunks.all(), limit=limit)
    return "\n\n".join(f"[score={score:.2f}] {chunk.text}" for score, chunk in matches if score > 0)
