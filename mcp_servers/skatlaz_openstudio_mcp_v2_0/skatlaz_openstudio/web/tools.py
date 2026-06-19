from pathlib import Path
import requests
from bs4 import BeautifulSoup


def scrape_page(url: str) -> dict:
    r = requests.get(url, timeout=20, headers={'User-Agent':'SkatlazOpenStudioMCP/2.0'})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title.string.strip() if soup.title and soup.title.string else ''
    desc = ''
    m = soup.find('meta', attrs={'name':'description'}) or soup.find('meta', attrs={'property':'og:description'})
    if m: desc = m.get('content','')
    images = [img.get('src') for img in soup.find_all('img') if img.get('src')][:20]
    text = ' '.join(soup.get_text(' ').split())[:5000]
    return {'url':url, 'title':title, 'description':desc, 'images':images, 'text':text}
