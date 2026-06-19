import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import AIService

service = AIService()


def _as_bool(value, default=True):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() not in ("0", "false", "no", "off", "não", "nao")


@csrf_exempt
def ask_view(request):
    if request.method == "GET":
        prompt = request.GET.get("q", "").strip()
        if not prompt:
            return JsonResponse({"error": "Parâmetro q obrigatório. Exemplo: /ask/?q=o que é django"}, status=400)
        result = service.ask(
            prompt,
            use_web=_as_bool(request.GET.get("use_web"), True),
            use_duckduckgo=_as_bool(request.GET.get("use_duckduckgo"), True),
            use_webdiver=_as_bool(request.GET.get("use_webdiver"), True),
            max_results=int(request.GET.get("max_results", 5)),
            min_score=float(request.GET.get("min_score", 0.75)),
        )
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False, "indent": 2})

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
        except Exception:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        prompt = data.get("prompt", "").strip()
        if not prompt:
            return JsonResponse({"error": "Campo 'prompt' é obrigatório"}, status=400)

        result = service.ask(
            prompt,
            use_web=_as_bool(data.get("use_web", True), True),
            use_duckduckgo=_as_bool(data.get("use_duckduckgo", True), True),
            use_webdiver=_as_bool(data.get("use_webdiver", True), True),
            max_results=int(data.get("max_results", 5)),
            min_score=float(data.get("min_score", 0.75)),
        )
        return JsonResponse(result, json_dumps_params={"ensure_ascii": False, "indent": 2})

    return JsonResponse({"error": "Método não suportado"}, status=405)


@csrf_exempt
def train_view(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        question = data.get("question")
        answer = data.get("answer")
        return JsonResponse(service.train(question, answer))
    return JsonResponse({"error": "POST only"}, status=405)


def search_view(request):
    query = request.GET.get("q", "").strip()
    return JsonResponse(service.ask(query), json_dumps_params={"ensure_ascii": False, "indent": 2})


def feeds_view(request):
    return JsonResponse({"feeds": service.feeds()}, json_dumps_params={"ensure_ascii": False, "indent": 2})
