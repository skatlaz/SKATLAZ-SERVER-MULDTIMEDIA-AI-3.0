from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("/ai/")),
    # API first, so /ask/ and /api/ask/ never fall into admin catch_all_view.
    path("", include("api.urls")),
    path("api/", include("api.urls")),
    path("ai/", include("ai_core.urls")),
    path("license/", include("skatlaz_server.license_system.urls")),
    path("admin/", admin.site.urls),
]
