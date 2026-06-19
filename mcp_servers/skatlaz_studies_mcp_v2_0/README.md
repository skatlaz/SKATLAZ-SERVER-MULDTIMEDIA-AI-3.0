# Skatlaz Studies MCP v2.0

MCP de estudos, chat, educação e criação visual para o Skatlaz Server AI 2.0.

## Recursos

- Chat Agent com memória local SQLite
- Integração opcional com Ollama
- Education Agent: resumos, quizzes, flashcards, planos de aula
- Creative Agent: banners HTML, apresentações PPTX, templates e canvas HTML
- Exportação de materiais de estudo em Markdown/HTML/PPTX
- API FastAPI estilo MCP
- CLI simples para testes

## Instalação Windows

```bat
install_windows.bat
run_server.bat
```

Servidor padrão:

```text
http://127.0.0.1:8045/docs
```

## Ollama opcional

Se quiser usar LLM local:

```bat
set OLLAMA_BASE_URL=http://localhost:11434
set OLLAMA_MODEL=llama3.1
```

Se Ollama não estiver ativo, o MCP usa respostas locais simples.

## Endpoints principais

- `POST /mcp/chat/ask`
- `GET /mcp/chat/history`
- `POST /mcp/education/summarize`
- `POST /mcp/education/quiz`
- `POST /mcp/education/flashcards`
- `POST /mcp/education/lesson-plan`
- `POST /mcp/creative/banner`
- `POST /mcp/creative/presentation`
- `POST /mcp/creative/canvas`

## Integração Skatlaz Server

Este MCP foi pensado para rodar como serviço separado e ser chamado pelo Skatlaz Server AI via HTTP/FastAPI.
