# Skatlaz Entertainment MCP v1.0

MCP/FastAPI para Conteúdo e Entretenimento do Skatlaz Server AI 2.0.

## Recursos
- Filmes e séries: busca local JSON/CSV, TVMaze sem chave, TMDb opcional com API key.
- Episódios: busca e resumo simples via TVMaze.
- Livros: Open Library sem chave, catálogo local JSON/CSV, resumo e PDF simples.
- Música: MusicBrainz sem chave, playlists locais, sugestões de arranjo e integração conceitual com Skatlaz MCP Music Producer.
- API estilo MCP com FastAPI.
- CLI para testes.

## Instalação Windows
```bat
install_windows.bat
```

## Rodar servidor
```bat
run_server.bat
```

Acesse:
- http://127.0.0.1:8092/docs
- http://127.0.0.1:8092/health

## Rodar CLI
```bat
python cli.py movie matrix
python cli.py tv friends
python cli.py book "dom casmurro"
python cli.py music "pink floyd"
python cli.py recommend movie sci-fi
```

## APIs usadas
- TVMaze: sem chave
- Open Library: sem chave
- MusicBrainz: sem chave, use User-Agent adequado
- TMDb: opcional, configure `TMDB_API_KEY` no `.env`

## Observação
Este MCP usa APIs públicas e fallback local. Para produção, respeite limites de uso e cache.
