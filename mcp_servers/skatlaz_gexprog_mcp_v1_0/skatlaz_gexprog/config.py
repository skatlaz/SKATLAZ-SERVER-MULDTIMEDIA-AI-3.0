from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GENERATED_DIR = ROOT / 'generated_projects'
RAG_DIR = ROOT / 'rag'
DATA_DIR = ROOT / 'data'
for p in [GENERATED_DIR, RAG_DIR, DATA_DIR]:
    p.mkdir(parents=True, exist_ok=True)

SUPPORTED_LANGUAGES = [
    'python','php','perl','cgi','html','css','javascript','typescript','nodejs',
    'java','kotlin','dart','flutter','kivy','c','cpp','csharp','assembler',
    'ruby','go','rust','zig','sql','bash','powershell','katlaz'
]
