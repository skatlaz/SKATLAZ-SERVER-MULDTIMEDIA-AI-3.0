import requests

BASE = "http://127.0.0.1:8098"

for path in [
    "/health",
    "/sports/local/search?q=Brazil",
    "/sports/worldcup/history",
    "/sports/wiki/summary?query=FIFA%20World%20Cup",
]:
    print(path)
    print(requests.get(BASE + path).json())
