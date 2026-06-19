# Skatlaz GexProg MCP v1.0

**GEX = Generate, Explain, Execute Programming**.

MCP de programação para o Skatlaz Server AI 2.0, focado em gerar, explicar, depurar, refatorar e documentar código por prompt de texto.

## Recursos

- Prompt → código
- Prompt → projeto completo
- README automático
- Debug, explain e refactor
- Auditoria rápida de segurança
- Pesquisa de pacotes em PyPI, npm, RubyGems, NuGet e crates.io
- GitHub README scraper básico
- RAG local de paradigmas de programação
- FastAPI MCP Server
- CLI para testes
- Compatível com Ollama + DeepSeek Coder ou APIs OpenAI-compatible

## Linguagens alvo

Python, PHP, Perl, CGI, HTML, CSS, JavaScript, TypeScript, NodeJS, Java, Kotlin, Dart, Flutter, Kivy, C, C++, C#, Assembler, Ruby, Go, Rust, Zig, SQL, Bash, PowerShell e Katlaz++.

## Instalação no Windows

```bat
install_windows.bat
```

## Rodar servidor MCP

```bat
run_server.bat
```

Abra:

```text
http://127.0.0.1:8077/docs
```

## Rodar CLI

```bat
run_cli.bat
```

## Usar com Ollama / DeepSeek Coder

Instale o Ollama e baixe um modelo coder:

```bat
ollama pull deepseek-coder:6.7b
```

Copie `.env.example` para `.env` ou defina variáveis:

```bat
set GEXPROG_PROVIDER=ollama
set OLLAMA_MODEL=deepseek-coder:6.7b
```

## Endpoints MCP

- `POST /mcp/gexprog/generate`
- `POST /mcp/gexprog/project`
- `POST /mcp/gexprog/explain`
- `POST /mcp/gexprog/debug`
- `POST /mcp/gexprog/refactor`
- `POST /mcp/gexprog/audit`
- `GET /mcp/package/search/{name}`
- `GET /mcp/github/readme/{owner}/{repo}`
- `GET /mcp/rag/search?q=...`

## Exemplo JSON

```json
{
  "prompt": "Crie uma API FastAPI para cadastro de produtos com SQLite",
  "language": "python",
  "name": "produtos_api"
}
```

## Observação

No modo padrão `local`, o sistema gera template básico. Para geração avançada, use Ollama/DeepSeek Coder ou API compatível.
