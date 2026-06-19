import requests
from fpdf import FPDF
from .config import DATA_DIR, OUTPUT_DIR
from .utils import load_json, filter_local, simple_summary

OPENLIB = "https://openlibrary.org"


def search_local_books(query: str = "", genre: str = ""):
    return filter_local(load_json(DATA_DIR / "books.json"), query, genre)


def openlibrary_search(query: str):
    r = requests.get(f"{OPENLIB}/search.json", params={"q": query, "limit":10}, timeout=20)
    r.raise_for_status()
    docs = r.json().get("docs", [])
    return [{"title": d.get("title"), "author": ", ".join(d.get("author_name", [])[:3]), "first_publish_year": d.get("first_publish_year"), "key": d.get("key"), "edition_count": d.get("edition_count"), "source":"OpenLibrary"} for d in docs]


def summarize_text(text: str, sentences: int = 5):
    return simple_summary(text, sentences)


def create_summary_pdf(title: str, summary: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, title)
    pdf.set_font("Helvetica", "", 12)
    pdf.multi_cell(0, 8, summary)
    out = OUTPUT_DIR / (title.lower().replace(" ", "_")[:40] + "_summary.pdf")
    pdf.output(str(out))
    return str(out)


def recommend_books(genre: str = "", query: str = ""):
    return search_local_books(query, genre)[:10]
