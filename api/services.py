import json
import re
import unicodedata
from db.feed import FeedRAG
from models.trainer import RAGTrainer
from db.database import Database
from .web_search import WebSearchAPI


def _norm(text):
    text = str(text or "").lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _keywords(text):
    stop = {
        "o", "a", "os", "as", "um", "uma", "de", "do", "da", "dos", "das",
        "e", "em", "no", "na", "nos", "nas", "que", "como", "para", "por",
        "sobre", "qual", "quais", "quem", "onde", "quando", "porque", "por que",
        "is", "the", "what", "how", "about", "with", "and", "or", "to", "of"
    }
    return [w for w in _norm(text).split() if len(w) > 2 and w not in stop]


class AIService:
    def __init__(self):
        self.feed = FeedRAG("rag/feed")
        self.rag = RAGTrainer()
        self.web = WebSearchAPI()

    def _save_question(self, prompt):
        db = Database()
        try:
            return db.save_question(prompt)
        finally:
            db.close()

    def _save_response(self, qid, source, content, score=0):
        db = Database()
        try:
            db.save_response(qid, source, content, score)
        finally:
            db.close()

    def _search_webdiver_tasks(self, prompt):
        """Search results already collected in Django Admin > Web diver tasks."""
        try:
            from ai_core.models import WebDiverTask
        except Exception:
            return None

        words = _keywords(prompt)
        if not words:
            return None

        tasks = WebDiverTask.objects.exclude(result_json={}).order_by("-updated_at", "-created_at")[:100]
        best_task = None
        best_score = 0
        best_text = ""

        for task in tasks:
            result_json = task.result_json or {}
            result_text = ""
            if isinstance(result_json, dict):
                result_text = result_json.get("result") or result_json.get("text") or result_json.get("content") or json.dumps(result_json, ensure_ascii=False)
            else:
                result_text = str(result_json)

            haystack = " ".join([
                task.title or "",
                task.url or "",
                task.task_prompt or "",
                task.logs or "",
                result_text or "",
            ])
            nh = _norm(haystack)
            score = sum(1 for w in words if w in nh)
            if score > best_score and result_text:
                best_score = score
                best_task = task
                best_text = result_text

        if best_task and best_score > 0:
            return {
                "answer": best_text,
                "source": best_task.url or f"webdiver_task:{best_task.id}",
                "provider": "webdiver_task",
                "score": float(best_score),
                "webdiver_task": {
                    "id": best_task.id,
                    "title": best_task.title,
                    "status": best_task.status,
                }
            }
        return None

    def ask(self, prompt, use_web=True, use_duckduckgo=True, use_webdiver=True, max_results=5, min_score=0.75):
        qid = self._save_question(prompt)
        notes = []

        feeds = self.feed.load_feeds()
        docs = [item.get("summary", "") for item in feeds]

        if docs:
            scores = self.rag.similarity_search(prompt, docs)
            idx = scores.argmax()
            best = feeds[idx]
            score = float(scores[idx])
            if score >= min_score:
                self._save_response(qid, best.get("source", "rag/feed"), best.get("summary", ""), score)
                return {
                    "question": prompt,
                    "answer": best.get("summary", ""),
                    "source": best.get("source", "rag/feed"),
                    "score": score,
                    "provider": "rag"
                }
            notes.append(f"RAG/feed encontrado, mas score baixo: {score}")
        else:
            notes.append("Nenhum feed encontrado em rag/feed/")

        if use_webdiver:
            wd = self._search_webdiver_tasks(prompt)
            if wd:
                self._save_response(qid, wd["source"], wd["answer"], wd.get("score", 0))
                wd["question"] = prompt
                wd["notes"] = notes
                return wd
            notes.append("Nenhum resultado compatível encontrado em Web diver tasks")

        if use_web and use_duckduckgo:
            web_results = self.web.duckduckgo(prompt, max_results=max_results)
            if web_results:
                # Try to read full pages using WebDiver/fallback requests.
                enriched = []
                for r in web_results[:max_results]:
                    url = r.get("url") or r.get("href")
                    page_text = self.web.read_url_text(url) if url else ""
                    if page_text:
                        enriched.append({**r, "page_text": page_text})

                if enriched:
                    answer = "\n\n".join([
                        f"{r.get('title','')}\n{r.get('page_text','')[:1800]}\nFonte: {r.get('url','')}"
                        for r in enriched[:3]
                    ])
                    provider = "duckduckgo_webdiver"
                else:
                    answer = "\n\n".join([
                        f"{r.get('title','')}\n{r.get('body','')}\nFonte: {r.get('url','')}"
                        for r in web_results[:3]
                    ])
                    provider = "duckduckgo"

                self._save_response(qid, provider, answer, 0.50)
                return {
                    "question": prompt,
                    "answer": answer,
                    "source": provider,
                    "provider": provider,
                    "results": web_results[:max_results],
                    "notes": notes,
                }
            notes.append("DuckDuckGo não retornou resultados")

        return {
            "question": prompt,
            "answer": "Nenhum feed encontrado em rag/feed/ e nenhuma busca web retornou resultados.",
            "provider": "none",
            "notes": notes,
        }

    def feeds(self):
        return self.feed.load_feeds()

    def train(self, question, answer):
        db = Database()
        try:
            db.train(question, answer)
        finally:
            db.close()
        return {"status": "trained"}
