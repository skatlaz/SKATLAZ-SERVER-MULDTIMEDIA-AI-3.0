import json
from pathlib import Path
from django.utils.text import slugify

try:
    from .gemini_mcp_builder import build_mcp_json
    from .template_scanner import scan_pugex_templates
except Exception:
    from ai_core.services.gemini_mcp_builder import build_mcp_json
    from ai_core.services.template_scanner import scan_pugex_templates

try:
    from ai_core.models import AIMCPAgent, AIMCPServer, AIGeneratedArtifact, TrainingDataset, RagCollection
except Exception:
    AIMCPAgent = AIMCPServer = AIGeneratedArtifact = TrainingDataset = RagCollection = None

MULTIMEDIA_ENGINES = {
    "image": {
        "default": "flux.1-dev",
        "options": ["flux.1-dev", "sdxl-turbo", "image-z-turbo", "grok-image", "openai-image"],
        "pipeline": ["prompt_enhance", "style", "reference_image", "generate", "upscale", "export"],
    },
    "video": {
        "default": "wan2.1", 
        "options": ["wan2.1", "open-sora", "cogvideox", "hunyuan-video", "grok-video"],
        "pipeline": ["script", "keyframes", "image_to_video", "frames", "ffmpeg_export"],
    },
    "audio": {
        "default": "bark-tts", 
        "options": ["bark-tts", "coqui-tts", "rvc", "demucs", "ffmpeg"],
        "pipeline": ["script", "voice", "tts", "master", "export"],
    },
    "rag": {
        "default": "sentence-transformers", 
        "options": ["sentence-transformers", "faiss", "chromadb", "webdiver", "pypdf", "python-docx"],
        "pipeline": ["ingest", "chunk", "embed", "retrieve", "augment", "answer"],
    },
    "code": {
        "default": "deepseek-code", 
        "options": ["deepseek-code", "deepseek-coder", "qwen-coder", "mistral", "ollama"],
        "pipeline": ["detect_language", "plan", "generate", "debug", "tests", "artifact"],
    },
}


def _base_config(task_type, engine=None):
    cfg = MULTIMEDIA_ENGINES.get(task_type, MULTIMEDIA_ENGINES.get("code"))
    chosen = engine or cfg["default"]
    return {
        "mcp_name": f"mcp_{task_type}",
        "engine": chosen,
        "available_engines": cfg["options"],
        "pipeline": cfg["pipeline"],
        "enabled": True,
        "local_first": True,
        "fallback_api": True,
        "output_dir": f"outputs/{task_type}/",
    }


def _training_package(task_type, prompt):
    return {
        "dataset_target": f"training/{task_type}/dataset.jsonl",
        "include_prompt": True,
        "include_generated_artifacts": True,
        "include_metadata": True,
        "sample": {
            "instruction": prompt,
            "task_type": task_type,
            "response_format": "json+mcp_artifact"
        },
        "commands": [
            "python manage.py skatlaz_prepare_finetune",
            "python manage.py skatlaz_index_rag",
        ]
    }


def run_task(task_type: str, prompt: str, language: str = "", target_os: str = "all", agent_slug: str = "", engine: str = ""):
    task_type = (task_type or "ask").lower().strip()
    agent = None
    if AIMCPAgent and agent_slug:
        agent = AIMCPAgent.objects.filter(slug=agent_slug, active=True).first()

    if task_type == "ask":
        task_type = "code" if language in ["python", "django", "javascript", "html", "css"] else "rag"

    data = build_mcp_json(task_type, prompt, language, target_os)
    data["skatlaz_mcp_config"] = _base_config(task_type, engine)
    data["deepseek_code"] = _base_config("code", "deepseek-code")
    data["training_package"] = _training_package(task_type, prompt)

    if task_type == "code":
        result = {"answer": "DeepSeek Code MCP programou o pacote inicial.", "action": "ai.generate_code", "mcp": data, "templates": scan_pugex_templates(language or "html")}
    elif task_type == "debug":
        result = {"answer": "Debug MCP preparado com errors_json por linguagem e sistema operacional.", "action": "ai.fix_error", "mcp": data, "errors_json": data.get("errors_json", {})}
    elif task_type == "image":
        result = {"answer": "Image MCP configurado para gerar imagem com motor selecionável.", "action": "ai.create_image", "mcp": data, "image_json": data.get("image_json", {})}
    elif task_type == "video":
        result = {"answer": "Video MCP configurado para roteiro, keyframes, image-to-video e exportação FFmpeg.", "action": "ai.create_video", "mcp": data}
    elif task_type == "audio":
        result = {"answer": "Audio MCP configurado para TTS, voz, masterização e exportação.", "action": "ai.create_audio", "mcp": data}
    elif task_type == "rag":
        result = {"answer": "RAG MCP configurado para ingestão, chunking, embeddings e resposta aumentada.", "action": "ai.rag", "mcp": data}
    elif task_type == "train":
        result = {"answer": "Treinamento MCP multimídia preparado para incluir novos conteúdos nos pacotes.", "action": "ai.train_multimedia_mcp", "mcp": data}
    else:
        result = {"answer": "Skatlaz Client processou a solicitação.", "action": "ai.chat", "mcp": data}

    if AIGeneratedArtifact:
        try:
            AIGeneratedArtifact.objects.create(title=f"{task_type}: {prompt[:60]}", task_type=task_type, agent=agent, input_prompt=prompt, output_json=result)
        except Exception:
            pass
    return result
