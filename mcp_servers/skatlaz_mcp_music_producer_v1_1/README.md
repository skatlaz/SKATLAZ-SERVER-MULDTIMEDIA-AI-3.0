# Skatlaz MCP Music Producer 1.1

Versão 1.0 estável para Windows, focada em:

- Análise de áudio MP3 / FLAC / WAV
- Detecção aproximada de BPM
- Análise de loudness/RMS/peak
- Separação de stems com Demucs
- Masterização automática com FFmpeg
- Exportação MP3 320 kbps e WAV
- Relatório JSON e TXT
- ZIP final do álbum
- Base preparada para integração MCP / Skatlaz Server AI

## Por que não inclui MusicGen/AudioCraft na 1.0?

MusicGen, AudioCraft, backing vocals por IA e violinos por IA ficam para a versão 2.0 porque são mais pesados e instáveis no Windows, principalmente com Python recente.

A versão 1.0 já resolve o fluxo de remasterização e organização do álbum.

## Instalação recomendada no Windows 11

Use Python 3.11.

```bat
py -3.11 -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

Instale também o FFmpeg e deixe no PATH.

Teste:

```bat
ffmpeg -version
demucs --help
```

## Como usar

Coloque seus arquivos em:

```text
input_album/
```

Formatos aceitos:

```text
.mp3
.wav
.flac
.ogg
.m4a
```

Execute:

```bat
python main.py
```

Saída:

```text
output_album/
├── masters_wav/
├── masters_mp3/
├── stems/
├── reports/
└── album_package.zip
```

## Exemplo com o álbum Buskplay AI-DSP Press

Você pode usar para o projeto:

```text
My Damn Blues Book - Busk Blues
Buskplay AI-DSP Press
```

O software vai gerar relatório por faixa e um ZIP final com masters e relatórios.


## Correções da versão 1.1

- Detecta FFmpeg em `C:\ffmpeg\bin\ffmpeg.exe` ou no PATH.
- Detecta Demucs antes de tentar separar stems.
- Se Demucs não estiver instalado, pula stems e continua a masterização.
- Se FFmpeg não estiver instalado, pula masterização/exportação MP3 e ainda gera relatórios.
- Relatórios não quebram mais com `KeyError` quando uma etapa falha.
- `check_deps.bat` mostra o status das dependências.

## Comandos úteis no Windows

```bat
py -3.11 -m venv venv
venv\Scriptsctivate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install demucs
check_deps.bat
python main.py
```

Para FFmpeg, extraia em:

```text
C:fmpeginfmpeg.exe
```

ou adicione essa pasta ao PATH.
