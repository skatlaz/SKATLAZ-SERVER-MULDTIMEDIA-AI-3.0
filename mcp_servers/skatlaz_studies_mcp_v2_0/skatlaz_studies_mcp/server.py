from fastapi import FastAPI
from pydantic import BaseModel, Field
from .core import SkatlazStudiesMCP

app = FastAPI(title="Skatlaz Studies MCP", version="2.0.0")
mcp = SkatlazStudiesMCP()

class ChatAskRequest(BaseModel):
    prompt: str
    user_id: str = "default"
    agent: str = "teacher"

class TextRequest(BaseModel):
    text: str
    style: str = "didático"

class TopicRequest(BaseModel):
    topic: str
    total: int = Field(default=10, ge=1, le=50)

class LessonPlanRequest(BaseModel):
    topic: str
    duration_minutes: int = 60

class BannerRequest(BaseModel):
    title: str
    subtitle: str = ""
    theme: str = "olive"

class PresentationRequest(BaseModel):
    title: str
    slides: list[str]
    subtitle: str = "Skatlaz Studies MCP"

class CanvasBlock(BaseModel):
    title: str
    text: str

class CanvasRequest(BaseModel):
    title: str
    blocks: list[CanvasBlock]
    theme: str = "clean"

class ImagePromptRequest(BaseModel):
    subject: str
    style: str = "Van Gogh"
    format: str = "banner"

@app.get("/")
def root():
    return {"name": "Skatlaz Studies MCP", "version": "2.0.0", "docs": "/docs"}

@app.post("/mcp/chat/ask")
def chat_ask(req: ChatAskRequest):
    return mcp.chat.ask(req.prompt, user_id=req.user_id, agent=req.agent)

@app.get("/mcp/chat/history")
def chat_history(user_id: str = "default", limit: int = 20):
    return {"history": mcp.chat.history(user_id, limit)}

@app.post("/mcp/education/summarize")
def summarize(req: TextRequest):
    return mcp.education.summarize(req.text, style=req.style)

@app.post("/mcp/education/explain")
def explain(req: LessonPlanRequest):
    return mcp.education.explain(req.topic, level="iniciante")

@app.post("/mcp/education/quiz")
def quiz(req: TopicRequest):
    return mcp.education.create_quiz(req.topic, total_questions=req.total)

@app.post("/mcp/education/flashcards")
def flashcards(req: TopicRequest):
    return mcp.education.create_flashcards(req.topic, total_cards=req.total)

@app.post("/mcp/education/lesson-plan")
def lesson_plan(req: LessonPlanRequest):
    return mcp.education.lesson_plan(req.topic, req.duration_minutes)

@app.post("/mcp/creative/banner")
def banner(req: BannerRequest):
    return mcp.creative.create_banner(req.title, req.subtitle, req.theme)

@app.post("/mcp/creative/presentation")
def presentation(req: PresentationRequest):
    return mcp.creative.create_presentation(req.title, req.slides, req.subtitle)

@app.post("/mcp/creative/canvas")
def canvas(req: CanvasRequest):
    return mcp.creative.create_canvas(req.title, [b.model_dump() for b in req.blocks], req.theme)

@app.post("/mcp/creative/image-prompt")
def image_prompt(req: ImagePromptRequest):
    return mcp.creative.image_prompt(req.subject, req.style, req.format)
