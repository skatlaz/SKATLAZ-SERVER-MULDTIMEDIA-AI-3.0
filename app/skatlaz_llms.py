from db.database import Database
from db.feed import FeedRAG
from models.trainer import RAGTrainer

class SkatlazLLMS:
    def __init__(self):
        self.db = Database()
        self.feed = FeedRAG()
        self.rag = RAGTrainer()

    def ask(self, prompt):
        qid = self.db.save_question(prompt)

        feed_data = self.feed.load_feeds()
        documents = [x["summary"] for x in feed_data]

        scores = self.rag.similarity_search(prompt, documents)

        best_idx = scores.argmax()
        best_result = feed_data[best_idx]

        self.db.save_response(
            qid,
            best_result["source"],
            best_result["summary"],
            float(scores[best_idx])
        )

        return {
            "answer": best_result["summary"],
            "source": best_result["source"],
            "score": float(scores[best_idx])
        }


if __name__ == "__main__":
    ai = SkatlazLLMS()
    resposta = ai.ask("últimas notícias sobre inteligência artificial")
    print(resposta)
