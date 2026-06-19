import json
from pathlib import Path
from ..config import OUTPUTS_DIR
from .llm import LLMClient

class EducationAgent:
    def __init__(self):
        self.llm = LLMClient()

    def summarize(self, text: str, style: str = "didático") -> dict:
        prompt = f"Resuma o texto em estilo {style}, com tópicos principais e conclusão:\n\n{text[:8000]}"
        summary = self.llm.ask(prompt)
        return {"summary": summary, "style": style}

    def explain(self, topic: str, level: str = "iniciante") -> dict:
        prompt = f"Explique {topic} para nível {level}, com exemplo simples e aplicação prática."
        return {"topic": topic, "level": level, "explanation": self.llm.ask(prompt)}

    def create_quiz(self, topic: str, total_questions: int = 10) -> dict:
        questions = []
        for i in range(1, total_questions + 1):
            questions.append({
                "id": i,
                "question": f"Questão {i} sobre {topic}: explique um conceito importante.",
                "options": ["A", "B", "C", "D"],
                "answer": "A",
                "explanation": f"Resposta explicada sobre {topic}."
            })
        out = {"topic": topic, "total_questions": total_questions, "questions": questions}
        (OUTPUTS_DIR / f"quiz_{self._safe(topic)}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        return out

    def create_flashcards(self, topic: str, total_cards: int = 10) -> dict:
        cards = [{"front": f"{topic} - conceito {i}", "back": f"Explicação do conceito {i} sobre {topic}."} for i in range(1, total_cards + 1)]
        out = {"topic": topic, "cards": cards}
        (OUTPUTS_DIR / f"flashcards_{self._safe(topic)}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
        return out

    def lesson_plan(self, topic: str, duration_minutes: int = 60) -> dict:
        plan = {
            "topic": topic,
            "duration_minutes": duration_minutes,
            "objectives": [f"Compreender {topic}", "Aplicar conceitos em exercícios", "Revisar pontos principais"],
            "sections": [
                {"title": "Introdução", "minutes": 10},
                {"title": "Explicação", "minutes": 25},
                {"title": "Exercícios", "minutes": 15},
                {"title": "Resumo", "minutes": 10},
            ]
        }
        return plan

    def build_study_markdown(self, title: str, text: str) -> dict:
        summary = self.summarize(text)["summary"]
        quiz = self.create_quiz(title, 5)
        md = f"# {title}\n\n## Resumo\n\n{summary}\n\n## Quiz\n"
        for q in quiz["questions"]:
            md += f"\n### {q['id']}. {q['question']}\nResposta: {q['answer']}\n"
        path = OUTPUTS_DIR / f"study_{self._safe(title)}.md"
        path.write_text(md, encoding="utf-8")
        return {"file": str(path), "markdown": md}

    def _safe(self, s: str) -> str:
        return "".join(c if c.isalnum() else "_" for c in s.lower())[:80]
