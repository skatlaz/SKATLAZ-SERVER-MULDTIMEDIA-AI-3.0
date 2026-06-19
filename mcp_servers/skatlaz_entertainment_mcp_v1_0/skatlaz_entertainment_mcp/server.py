from fastapi import FastAPI, Query
from pydantic import BaseModel
from .movies import tvmaze_search_show, tvmaze_episodes, tmdb_search_movie, recommend_movies
from .books import openlibrary_search, summarize_text, create_summary_pdf, recommend_books
from .music import musicbrainz_artist, smart_playlist, arrangement_suggestions, search_local_music

app = FastAPI(title="Skatlaz Entertainment MCP", version="1.0.0")

class TextPayload(BaseModel):
    title: str = "Resumo"
    text: str
    sentences: int = 5

@app.get("/health")
def health():
    return {"ok": True, "mcp": "skatlaz_entertainment_mcp", "version": "1.0.0"}

@app.get("/mcp/tools")
def tools():
    return {"tools":[
        "movies.search_tv", "movies.episodes", "movies.search_tmdb", "movies.recommend",
        "books.search", "books.summarize", "books.summary_pdf", "books.recommend",
        "music.artist", "music.playlist", "music.arrangement", "music.local_search"
    ]}

@app.get("/movies/search_tv")
def movies_search_tv(q: str): return tvmaze_search_show(q)

@app.get("/movies/episodes/{show_id}")
def movies_episodes(show_id: int): return tvmaze_episodes(show_id)

@app.get("/movies/search_tmdb")
def movies_tmdb(q: str): return tmdb_search_movie(q)

@app.get("/movies/recommend")
def movies_recommend(genre: str = "", q: str = ""): return recommend_movies(genre, q)

@app.get("/books/search")
def books_search(q: str): return openlibrary_search(q)

@app.post("/books/summarize")
def books_summarize(payload: TextPayload): return {"summary": summarize_text(payload.text, payload.sentences)}

@app.post("/books/summary_pdf")
def books_pdf(payload: TextPayload): return {"file": create_summary_pdf(payload.title, summarize_text(payload.text, payload.sentences))}

@app.get("/books/recommend")
def books_recommend(genre: str = "", q: str = ""): return recommend_books(genre, q)

@app.get("/music/artist")
def music_artist(q: str): return musicbrainz_artist(q)

@app.get("/music/playlist")
def music_playlist(mood: str = "", genre: str = ""): return smart_playlist(mood, genre)

@app.get("/music/arrangement")
def music_arrangement(style: str): return {"style": style, "suggestions": arrangement_suggestions(style)}

@app.get("/music/local_search")
def music_local(q: str = "", genre: str = ""): return search_local_music(q, genre)
