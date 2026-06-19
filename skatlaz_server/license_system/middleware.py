from django.shortcuts import redirect
from .core import is_activated


class SkatlazLicenseMiddleware:
    """Bloqueia o sistema quando SKATLAZ_LICENSE_ENFORCE=True e não há licença válida."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.conf import settings
        enforce = getattr(settings, "SKATLAZ_LICENSE_ENFORCE", True)
        allowed_prefixes = ("/license/", "/static/", "/media/", "/favicon.ico")
        if enforce and not request.path.startswith(allowed_prefixes):
            if not is_activated():
                return redirect("/license/activate/")
        return self.get_response(request)
