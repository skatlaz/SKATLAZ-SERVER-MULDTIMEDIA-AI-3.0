from skatlaz_studies_mcp.core import SkatlazStudiesMCP

mcp = SkatlazStudiesMCP()

print("=== Skatlaz Studies MCP v2.0 ===")
print(mcp.chat.ask("Explique inteligência artificial em linguagem simples", user_id="demo"))
print(mcp.education.create_quiz("Inteligência Artificial", total_questions=5))
print(mcp.education.create_flashcards("Python", total_cards=5))
print(mcp.creative.create_banner("Skatlaz Studies", "AI for learning and creativity"))
print(mcp.creative.create_presentation("Aula de IA", ["O que é IA", "Machine Learning", "LLMs", "Aplicações"]))
