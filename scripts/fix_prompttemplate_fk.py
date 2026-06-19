"""
Corrige o erro no admin de PromptTemplate:
IntegrityError: FOREIGN KEY constraint failed

Uso no Windows, dentro da pasta do projeto:
    python scripts/fix_prompttemplate_fk.py

O script limpa referências órfãs/legadas de ai_core_aiagent.prompt_template_id
sem apagar agentes, prompts ou dados importantes.
"""
from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "db.sqlite3"

if not DB_PATH.exists():
    raise SystemExit(f"Banco não encontrado: {DB_PATH}")

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

def table_exists(name):
    cur.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,))
    return cur.fetchone() is not None

if not table_exists("ai_core_aiagent") or not table_exists("ai_core_prompttemplate"):
    print("Nada para corrigir: tabela legada ai_core_aiagent ou ai_core_prompttemplate não existe.")
    con.close()
    raise SystemExit(0)

cur.execute("PRAGMA foreign_keys=OFF")

# Remove referências para prompts inexistentes.
cur.execute(
    """
    UPDATE ai_core_aiagent
       SET prompt_template_id = NULL
     WHERE prompt_template_id IS NOT NULL
       AND prompt_template_id NOT IN (SELECT id FROM ai_core_prompttemplate)
    """
)
orphans = cur.rowcount

con.commit()
cur.execute("PRAGMA foreign_keys=ON")
checks = list(cur.execute("PRAGMA foreign_key_check"))
con.close()

print(f"Referências órfãs limpas: {orphans}")
if checks:
    print("Ainda existem problemas de FK:")
    for row in checks:
        print(row)
else:
    print("OK: foreign_key_check sem erros.")
