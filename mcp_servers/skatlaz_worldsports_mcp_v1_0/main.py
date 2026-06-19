import sys
import uvicorn
from skatlaz_worldsports_mcp.localdb import LocalSportsDB
from skatlaz_worldsports_mcp.wiki import wikipedia_summary
from skatlaz_worldsports_mcp.rss import read_rss
from skatlaz_worldsports_mcp.reports import markdown_report

def demo():
    db = LocalSportsDB("data")
    print("=== Local search: Brazil ===")
    print(db.search("Brazil"))
    print("\n=== World Cup history ===")
    print(db.list_worldcups())
    print("\n=== Wikipedia summary ===")
    print(wikipedia_summary("FIFA World Cup"))
    print("\n=== Report ===")
    print(markdown_report("Skatlaz Sports Demo", [("Brazil", db.search("Brazil")), ("World Cup", db.list_worldcups())], "reports/demo_report.md"))

def server():
    uvicorn.run("skatlaz_worldsports_mcp.server:app", host="127.0.0.1", port=8098, reload=False)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        server()
    else:
        demo()
