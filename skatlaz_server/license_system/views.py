from django.shortcuts import render, redirect
from django.contrib import messages
from .core import save_license, load_license, machine_fingerprint


def activate(request):
    current = None
    try:
        current = load_license()
    except Exception:
        current = None
    if request.method == "POST":
        license_key = request.POST.get("license_key", "").strip()
        try:
            payload = save_license(license_key)
            messages.success(request, f"Skatlaz Server AI ativado: {payload.get('edition', 'COMMERCIAL')}")
            return redirect("license_status")
        except Exception as exc:
            messages.error(request, f"Licença inválida: {exc}")
    return render(request, "license_system/activate.html", {"current": current, "machine": machine_fingerprint()})


def status(request):
    license_data = None
    error = None
    try:
        license_data = load_license()
    except Exception as exc:
        error = str(exc)
    return render(request, "license_system/status.html", {"license_data": license_data, "error": error, "machine": machine_fingerprint()})
