# Skatlaz WorldSports MCP v1.0

MCP funcional para esportes mundiais: resultados, históricos, times, atletas, campeonatos,
Olimpíadas, Copa do Mundo, RSS, Wikipedia/Wikidata e arquivos locais JSON/CSV.

## Recursos

- FastAPI MCP Server
- CLI de teste
- Base local JSON para times, atletas, competições e históricos
- Pesquisa Wikipedia REST
- Wikidata SPARQL
- RSS esportivo
- TheSportsDB opcional
- Football-Data.org opcional
- Exportação JSON/CSV
- Relatórios Markdown

## Instalação Windows

```bat
install_windows.bat
run_server.bat
```

Depois abra:

```text
http://127.0.0.1:8097/docs
```

## Variáveis opcionais

```bat
set THESPORTSDB_API_KEY=3
set FOOTBALL_DATA_API_KEY=SUA_CHAVE
```

TheSportsDB permite chave de teste `3` para endpoints públicos.

## Exemplos de endpoints

```text
GET /health
GET /sports/local/search?q=brasil
GET /sports/wiki/summary?query=FIFA World Cup
GET /sports/wikidata/search?query=Olympic Games
GET /sports/rss?url=https://ge.globo.com/rss/ge/futebol/
GET /sports/thesportsdb/team?name=Brazil
GET /sports/report/worldcup
```

## Integração Skatlaz Server AI

Use este MCP como serviço externo e chame endpoints via MCP Router.
