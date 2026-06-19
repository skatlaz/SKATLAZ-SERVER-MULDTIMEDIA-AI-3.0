from .modules.chat import ChatAgent
from .modules.education import EducationAgent
from .modules.creative import CreativeAgent

class SkatlazStudiesMCP:
    def __init__(self):
        self.chat = ChatAgent()
        self.education = EducationAgent()
        self.creative = CreativeAgent()
