from skatlaz_infotoday_mcp.core import SkatlazInfoTodayMCP

mcp = SkatlazInfoTodayMCP("data")

print("=== Skatlaz InfoToday MCP CLI ===")
print("Exemplos:")
print("- clima em São Paulo")
print("- rota de Avenida Paulista São Paulo para Avenida Faria Lima São Paulo")
print("- quero uma oficina mecanica")
print("- pesquise Python na Wikipedia")
print("Digite sair para encerrar.")

while True:
    prompt = input("\nInfoToday> ").strip()
    if prompt.lower() in {"sair", "exit", "quit"}:
        break
    print(mcp.ask(prompt))
