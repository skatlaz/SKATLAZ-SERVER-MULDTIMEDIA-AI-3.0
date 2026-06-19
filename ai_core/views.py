import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .services.mcp_runtime import run_task, MULTIMEDIA_ENGINES


def client_home(request):
    return render(request, "ai_core/skatlaz_client_home.html", {"engines": MULTIMEDIA_ENGINES})


def mcp_config(request):
    return JsonResponse({"mcp_engines": MULTIMEDIA_ENGINES}, json_dumps_params={"ensure_ascii": False, "indent": 2})


def _load_mcp_registry():
    from pathlib import Path
    path = Path(__file__).resolve().parent / "mcp_registry.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"version": "3.0.0", "mcp_servers": [], "pipelines": {}}


def mcp_registry(request):
    return JsonResponse(_load_mcp_registry(), json_dumps_params={"ensure_ascii": False, "indent": 2})


def pipelines(request):
    reg = _load_mcp_registry()
    return JsonResponse({"version": reg.get("version"), "pipelines": reg.get("pipelines", {}), "mcp_servers": reg.get("mcp_servers", [])}, json_dumps_params={"ensure_ascii": False, "indent": 2})

@csrf_exempt
def mcp_task(request):
    if request.method == "GET":
        return render(request, "ai_core/mcp_task.html")
    payload = request.POST.dict()
    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except Exception:
            payload = {}
    result = run_task(
        payload.get("task_type", "code"),
        payload.get("prompt", ""),
        payload.get("language", "html"),
        payload.get("target_os", "all"),
        payload.get("agent_slug", ""),
        payload.get("engine", ""),
    )
    return JsonResponse(result, json_dumps_params={"ensure_ascii": False, "indent": 2})
