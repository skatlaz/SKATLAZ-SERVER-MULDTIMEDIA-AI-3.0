import re
import requests

try:
    from duckduckgo_search import DDGS
except Exception:
    DDGS = None


class WebSearchAPI:
    def duckduckgo(self, query, max_results=5):
        if DDGS is None:
            return []
        results = []
        try:
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": r.get("title", ""),
                        "body": r.get("body", ""),
                        "url": r.get("href", "")
                    })
        except Exception:
            return []
        return results

    def read_url_text(self, url):
        if not url:
            return ""
        # Preferred path: WebDiver package, when available.
        for import_path in ("webdiver.web_diver", "webdiver"):
            try:
                if import_path == "webdiver.web_diver":
                    from webdiver.web_diver import www_diver
                else:
                    from webdiver import www_diver
                result = www_diver(uri=url, _type="text")
                if result:
                    return self._clean_text(result)
            except Exception:
                pass

        # Fallback: direct HTTP text extraction.
        try:
            headers = {"User-Agent": "SkatlazServerAI/2.0"}
            html = requests.get(url, headers=headers, timeout=12).text
            return self._clean_text(html)
        except Exception:
            return ""

    def _clean_text(self, text):
        text = str(text or "")
        text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
        text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def wikipedia(self, query):
        url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{query}"
        return requests.get(url, timeout=12).json()

    def github(self, query):
        url = f"https://api.github.com/search/repositories?q={query}"
        return requests.get(url, timeout=12).json()

    def pypi(self, package):
        url = f"https://pypi.org/pypi/{package}/json"
        return requests.get(url, timeout=12).json()
