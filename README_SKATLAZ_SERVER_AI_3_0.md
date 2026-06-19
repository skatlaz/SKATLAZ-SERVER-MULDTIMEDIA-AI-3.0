# Skatlaz Server AI 3.0 — MCP Pipelines Edition

Cliente default: `http://localhost:8000/`

## Novidades 3.0

- Cliente Skatlaz 3.0 com seleção de pipelines MCP.
- Registry JSON em `/ai/registry/` e pipelines em `/ai/pipelines/`.
- MCPs anexados incluídos em `mcp_servers/`.
- BAT único para Windows: `start_all_mcp_servers_and_skatlaz_3_0.bat`.
- DeepSeek Code como Code MCP padrão.
- OpenStudio para imagem, vídeo, áudio, TTS/STT, OCR e FFmpeg.
- Treinamento MCP multimídia com JSONL, RAG index e preparação LoRA/QLoRA.

## Como executar

```bat
start_all_mcp_servers_and_skatlaz_3_0.bat
```

Depois abra:

```text
http://localhost:8000/
```

## Endpoints

```text
/ai/
/ai/config/
/ai/registry/
/ai/pipelines/
/ai/mcp-task/
/admin/
```

## Portas MCP

- GexProg DeepSeek Code: 8077
- Money: 8020
- Studies: 8045
- OpenStudio: 8088
- Entertainment: 8092
- InfoToday: 8093
- Music Producer 1.1: 8787
- Music Producer 2.0: 8788
- SurfTask: 8790

Os MCPs Office e WorldSports usam `python main.py server` conforme o pacote original.
