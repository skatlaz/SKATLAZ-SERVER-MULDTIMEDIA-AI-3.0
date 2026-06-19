import os, sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skatlaz_server.settings")
import django; django.setup()
from skatlaz_server.license_system.core import save_license, machine_fingerprint
print("Machine fingerprint:", machine_fingerprint())
key = input("Cole a licença SKZ20C: ").strip()
payload = save_license(key)
print("Licença ativada:", payload)
