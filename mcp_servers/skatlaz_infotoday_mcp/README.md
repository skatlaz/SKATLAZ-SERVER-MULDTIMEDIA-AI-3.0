# Skatlaz InfoToday MCP

MCP cotidiano para o Skatlaz Server AI 2.0.

Inclui:

- Pesquisa e resumo: Wikipedia, arXiv e web básico
- Meteorologia: Open-Meteo sem chave de API
- Mapas: OpenStreetMap/Nominatim
- Rotas: OSRM público
- Lista Amarela local: JSON/CSV/TXT
- Contatos locais
- Notícias/web reader base
- API FastAPI estilo MCP
- CLI simples

## Instalação Windows

```bat
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Rodar servidor MCP

```bat
run_server.bat
```

ou:

```bat
python -m uvicorn server:app --host 127.0.0.1 --port 8092 --reload
```

Abra:

```text
http://127.0.0.1:8092/docs
```

## Exemplos de prompt

```text
Quero uma oficina mecânica em São Paulo
```

```text
Como está o clima em São Paulo hoje?
```

```text
Trace rota de Avenida Paulista para Faria Lima
```

```text
Pesquise artigos sobre generative AI no arXiv
```

## Observação

Alguns serviços públicos, como Nominatim e OSRM, têm limites de uso. Para produção, use cache local ou hospede instâncias próprias.
