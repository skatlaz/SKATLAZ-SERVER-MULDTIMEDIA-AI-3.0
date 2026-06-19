# Skatlaz Server AI 2.0 · MCP Multimídia

Recursos adicionados:

- Página inicial default do cliente em `/ai/` e `/ai/client/`.
- Endpoint JSON de configuração em `/ai/config/`.
- Endpoint de execução em `/ai/mcp-task/`.
- Image MCP: Flux, SDXL Turbo, Image Z-Turbo, Grok Image e OpenAI Image.
- Video MCP: Wan, Open-Sora, CogVideoX, Hunyuan Video e Grok Video.
- Audio MCP: Bark TTS, Coqui TTS, RVC, Demucs e FFmpeg.
- RAG MCP: Sentence Transformers, FAISS, ChromaDB, WebDiver, PyPDF e python-docx.
- Code MCP com DeepSeek Code / DeepSeek Coder / Qwen Coder / Ollama.
- Treinamento MCP multimídia com pacote JSONL para incluir prompts, artefatos e metadados.

## Como rodar

```bash
python manage.py migrate
python manage.py runserver
```

Abra:

```text
http://127.0.0.1:8000/ai/
```

## Exemplo de POST

```json
{
  "task_type": "video",
  "engine": "wan2.1",
  "prompt": "Crie um vídeo publicitário para o Skatlaz Server 2.0 com imagem, narração e roteiro",
  "language": "python",
  "target_os": "all",
  "agent_slug": "skatlaz-client-agent"
}
```

## Treinamento MCP multimídia

Use o tipo `train` no cliente ou envie via API. O retorno inclui `training_package` com destino JSONL, amostra de instrução, formato de resposta e comandos de preparação.
