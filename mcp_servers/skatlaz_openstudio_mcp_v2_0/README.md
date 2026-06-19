# Skatlaz OpenStudio MCP v2.0

MCP multimídia para o Skatlaz Server AI: áudio, vídeo, imagem, OCR, TTS, legendas, canvas, web scraping e publicação.

## Recursos

- Áudio: info, normalização, ganho, fade, efeitos básicos.
- Vídeo: info, filtros básicos, thumbnails.
- Imagem: filtros, capas de livros/discos/posters, QR Code.
- OCR: texto em imagem e QR/barcode.
- TTS: texto para voz com gTTS.
- Legendas: geração SRT simples.
- Canvas: HTML/CSS com template Skatlaz.
- Web: scraping de title, description, imagens e texto.
- Publishing: exportação TXT para PDF/DOCX.

## Instalação Windows

```bat
install_windows.bat
```

Também instale FFmpeg e adicione `C:\ffmpeg\bin` ao PATH.
Para OCR, instale Tesseract OCR.

## Rodar servidor MCP

```bat
run_server.bat
```

Acesse:

```text
http://127.0.0.1:8088/docs
```

## Exemplos de prompts MCP

- Crie uma capa para o livro "My Damn Blues Book".
- Leia o texto de uma imagem e exporte em PDF.
- Gere locução em português para este eBook.
- Crie uma miniatura do vídeo no segundo 3.
- Aplique filtro preto e branco no vídeo.
- Faça scraping de um site e retorne title, metatags e imagens.

## Integração sugerida

- Skatlaz Music Producer MCP
- Skatlaz Studies MCP
- Skatlaz SurfTask MCP
- Skatlaz Office AI Worker MCP
- Buskplay AI-DSP Press
