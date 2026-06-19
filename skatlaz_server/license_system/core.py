import base64
import json
import hashlib
import platform
import uuid
from pathlib import Path
from datetime import datetime, timezone
from django.conf import settings
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

PRODUCT_ID = "skatlaz-server-ai-2.0-commercial"
LICENSE_FILE = Path(getattr(settings, "SKATLAZ_LICENSE_FILE", settings.BASE_DIR / "license.json"))
PUBLIC_KEY_FILE = Path(__file__).resolve().parent / "public_key.pem"


def _b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64u_decode(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + pad).encode("ascii"))


def canonical_payload(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def machine_fingerprint() -> str:
    """ID offline da instalação. Pode fixar SKATLAZ_MACHINE_ID no settings.py para VPS/cliente."""
    forced = getattr(settings, "SKATLAZ_MACHINE_ID", "")
    raw = "|".join([
        forced,
        platform.node(),
        platform.system(),
        platform.machine(),
        hex(uuid.getnode()),
        str(settings.BASE_DIR),
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def decode_license(license_key: str) -> dict:
    parts = license_key.strip().split(".")
    if len(parts) != 3 or parts[0] != "SKZ20C":
        raise ValueError("Formato de licença inválido")
    payload = json.loads(_b64u_decode(parts[1]).decode("utf-8"))
    signature = _b64u_decode(parts[2])
    public_key = serialization.load_pem_public_key(PUBLIC_KEY_FILE.read_bytes())
    public_key.verify(
        signature,
        canonical_payload(payload),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )
    if payload.get("product") != PRODUCT_ID:
        raise ValueError("Licença não pertence a este produto")
    expires = payload.get("expires")
    if expires:
        exp = datetime.fromisoformat(expires.replace("Z", "+00:00"))
        if exp < datetime.now(timezone.utc):
            raise ValueError("Licença expirada")
    bound = payload.get("machine")
    if bound and bound != machine_fingerprint():
        raise ValueError("Licença vinculada a outra instalação")
    return payload


def save_license(license_key: str) -> dict:
    payload = decode_license(license_key)
    LICENSE_FILE.write_text(json.dumps({"license_key": license_key, "payload": payload}, indent=2, ensure_ascii=False), encoding="utf-8")
    return payload


def load_license() -> dict | None:
    if not LICENSE_FILE.exists():
        return None
    data = json.loads(LICENSE_FILE.read_text(encoding="utf-8"))
    payload = decode_license(data["license_key"])
    return {"license_key": data["license_key"], "payload": payload}


def is_activated() -> bool:
    try:
        return load_license() is not None
    except Exception:
        return False
