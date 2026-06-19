import json
import os
import re
from typing import Any, Dict

LANG_ALIASES = {"c#": "csharp", "c++": "cpp", "html/css": "html", "asm": "assembler"}


def normalize_language(language: str = "") -> str:
    lang = (language or "").strip().lower()
    return LANG_ALIASES.get(lang, lang or "generic")


def extract_hashtags(prompt: str):
    return re.findall(r"#([\w\-]+)", prompt or "")


def fallback_mcp(task_type: str, prompt: str, language: str = "", target_os: str = "all") -> Dict[str, Any]:
    lang = normalize_language(language)
    tags = extract_hashtags(prompt)
    base = {
        "mcp_version": "skatlaz-mcp-1.1",
        "task_type": task_type,
        "language": lang,
        "target_os": target_os or "all",
        "prompt": prompt or "",
        "hashtags": tags,
        "commands": [],
        "pipeline": [],
        "admin_editable": True,
    }
    if task_type == "code":
        base.update({
            "action": "ai.generate_code",
            "commands": ["detect_language", "load_language_commands_json", "scan_pugex_templates", "generate_source", "return_files"],
            "language_commands_json": {
                "html": ["create semantic HTML", "link CSS", "validate accessibility"],
                "python": ["create module", "add type hints", "run tests"],
                "csharp": ["create project", "compile", "run"],
                "assembler": ["select assembler", "compile", "link"],
                "c": ["create source", "compile with gcc/clang", "run"],
                "cpp": ["create source", "compile with g++/clang++", "run"],
                "kotlin": ["create activity/layout", "build gradle", "run emulator"],
            },
            "templates_path": f"/pugex/{lang}/templates/",
            "templates_json": {"path": f"/pugex/{lang}/templates/", "items": []},
        })
    elif task_type == "debug":
        base.update({
            "action": "ai.fix_error",
            "commands": ["detect_os", "detect_language", "load_errors_json", "explain_error", "suggest_patch"],
            "errors_json": {
                "windows": ["PATH", "permissions", "missing dll", "venv", "powershell syntax"],
                "linux": ["permission denied", "missing package", "systemd", "gcc headers"],
                "macosx": ["xcode tools", "codesign", "brew dependency"],
                "android": ["gradle", "sdk", "manifest", "emulator"],
                "ios": ["xcode", "provisioning", "simulator", "cocoapods"],
            },
        })
    elif task_type == "image":
        base.update({
            "action": "ai.create_image",
            "provider": "huggingface/image-zturbo",
            "commands": ["extract_hashtags", "merge_cinewiz_json", "enhance_prompt", "generate_image"],
            "image_json": {
                "zturbo_best_commands": ["high detail", "cinematic light", "sharp focus", "clean composition"],
                "cinewiz_tags": tags,
                "negative_prompt": "low quality, distorted, blurry, watermark, bad anatomy",
            },
        })
    elif task_type == "documents":
        base.update({
            "action": "ai.documents",
            "commands": ["detect_document_type", "load_docs_template_json", "generate_or_transform", "export"],
            "documents_json": {
                "formats": ["pdf", "pptx", "xlsx", "docx", "html", "css", "txt", "json"],
                "template_file": "docs_template.json",
            },
        })
    return {"mcp": base, "errors_json": base.get("errors_json", {}), "templates_json": base.get("templates_json", {}), "image_json": base.get("image_json", {}), "documents_json": base.get("documents_json", {})}


def build_mcp_json(task_type: str, prompt: str = "", language: str = "", target_os: str = "all") -> Dict[str, Any]:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return fallback_mcp(task_type, prompt, language, target_os)
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        ask = f"""
Crie um JSON MCP válido para Skatlaz Server AI.
Tipo: {task_type}
Linguagem: {language}
Sistema: {target_os}
Prompt: {prompt}
Responda apenas JSON, sem markdown.
"""
        resp = client.models.generate_content(model=os.environ.get("GEMINI_MODEL", "gemini-1.5-flash"), contents=ask)
        text = getattr(resp, "text", "") or ""
        text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(text)
    except Exception as exc:
        data = fallback_mcp(task_type, prompt, language, target_os)
        data["gemini_error"] = str(exc)
        return data
