from fastapi import FastAPI
from pydantic import BaseModel
from skatlaz_gexprog.generator import CodeGenerator
from skatlaz_gexprog.packages import PackageExplorer
from skatlaz_gexprog.github_scraper import GitHubScraper
from skatlaz_gexprog.rag import SimpleRAG
from skatlaz_gexprog.security import quick_code_audit

app = FastAPI(title='Skatlaz GexProg MCP v1.0', version='1.0.0')
gen = CodeGenerator(); pkg = PackageExplorer(); gh = GitHubScraper(); rag = SimpleRAG()

class PromptRequest(BaseModel):
    prompt: str
    language: str | None = None
    name: str | None = None

class CodeRequest(BaseModel):
    code: str
    language: str = 'python'
    error: str = ''

@app.get('/')
def home():
    return {'name':'Skatlaz GexProg MCP','version':'1.0','tools':['generate','project','explain','debug','refactor','packages','github','rag','audit']}

@app.post('/mcp/gexprog/generate')
def generate(req: PromptRequest):
    return gen.generate_code(req.prompt, req.language)

@app.post('/mcp/gexprog/project')
def project(req: PromptRequest):
    return gen.create_project(req.prompt, req.language, req.name)

@app.post('/mcp/gexprog/explain')
def explain(req: CodeRequest):
    return {'explanation': gen.explain(req.code, req.language)}

@app.post('/mcp/gexprog/debug')
def debug(req: CodeRequest):
    return {'fixed': gen.debug(req.code, req.error, req.language)}

@app.post('/mcp/gexprog/refactor')
def refactor(req: CodeRequest):
    return {'refactored': gen.refactor(req.code, req.language)}

@app.post('/mcp/gexprog/audit')
def audit(req: CodeRequest):
    return quick_code_audit(req.code)

@app.get('/mcp/package/search/{name}')
def package_search(name: str):
    return {'query': name, 'results': pkg.search_all(name)}

@app.get('/mcp/github/readme/{owner}/{repo}')
def github_readme(owner: str, repo: str):
    return gh.repo_readme(f'{owner}/{repo}')

@app.get('/mcp/rag/docs')
def rag_docs():
    return {'docs': rag.list_docs()}

@app.get('/mcp/rag/search')
def rag_search(q: str):
    return {'query': q, 'results': rag.search(q)}
