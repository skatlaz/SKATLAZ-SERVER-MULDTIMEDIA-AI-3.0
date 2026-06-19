import requests

BASE = 'http://127.0.0.1:8088'
print(requests.get(BASE + '/').json())
print(requests.post(BASE + '/image/cover', json={
    'title':'My Damn Blues Book',
    'subtitle':'Buskplay AI-DSP Press',
    'output_name':'my_damn_blues_book_cover.png'
}).json())
print(requests.post(BASE + '/tts', json={
    'text':'Bem-vindo ao Skatlaz OpenStudio MCP.',
    'lang':'pt',
    'output_name':'welcome.mp3'
}).json())
