import requests
from bs4 import BeautifulSoup

class GitHubScraper:
    def repo_readme(self, owner_repo: str):
        # tenta raw README primeiro
        for branch in ['main','master']:
            url=f'https://raw.githubusercontent.com/{owner_repo}/{branch}/README.md'
            r=requests.get(url,timeout=20)
            if r.status_code==200:
                return {'repo':owner_repo,'branch':branch,'readme':r.text[:20000]}
        return {'repo':owner_repo,'error':'README.md nao encontrado'}

    def repo_page_meta(self, url: str):
        r=requests.get(url,timeout=20,headers={'User-Agent':'SkatlazGexProg/1.0'})
        r.raise_for_status()
        soup=BeautifulSoup(r.text,'html.parser')
        title=soup.title.text.strip() if soup.title else ''
        desc=soup.find('meta',attrs={'name':'description'})
        return {'url':url,'title':title,'description': desc.get('content','') if desc else ''}
