import sys
from skatlaz_entertainment_mcp.movies import tvmaze_search_show, recommend_movies
from skatlaz_entertainment_mcp.books import openlibrary_search, recommend_books
from skatlaz_entertainment_mcp.music import musicbrainz_artist, smart_playlist, arrangement_suggestions

cmd = sys.argv[1] if len(sys.argv)>1 else "help"
arg = " ".join(sys.argv[2:]) if len(sys.argv)>2 else ""

if cmd == "movie": print(tvmaze_search_show(arg))
elif cmd == "tv": print(tvmaze_search_show(arg))
elif cmd == "book": print(openlibrary_search(arg))
elif cmd == "music": print(musicbrainz_artist(arg))
elif cmd == "playlist": print(smart_playlist(arg, ""))
elif cmd == "arrange": print(arrangement_suggestions(arg))
elif cmd == "recommend":
    kind = sys.argv[2] if len(sys.argv)>2 else "movie"
    genre = sys.argv[3] if len(sys.argv)>3 else ""
    print(recommend_movies(genre) if kind == "movie" else recommend_books(genre))
else:
    print("Uso: python cli.py movie <nome> | book <titulo> | music <artista> | playlist <mood> | arrange <style> | recommend movie <genre>")
