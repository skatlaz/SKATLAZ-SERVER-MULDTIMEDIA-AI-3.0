# Skatlaz MCP Music Producer 2.0

Buskplay AI-DSP Press / Skatlaz Server AI module for album analysis, stems, remastering, ZIP export and prompt-based music production planning.

## What works in stable mode

- Analyze MP3, FLAC and WAV
- Separate stems with Demucs when installed
- Remaster with FFmpeg
- Export WAV / MP3
- Generate album ZIP
- Generate production reports
- Generate arrangement plans for rain, birds, bells, piano, strings, backing vocals, synths and extra guitars
- FastAPI MCP-ready server

## Optional 2.0 AI mode

MusicGen / AudioCraft is isolated in `skatlaz_music_producer/ai_generators/musicgen_adapter.py`.
It is optional because it is heavy and can be unstable on Windows.

Install only when needed:

```bat
install_optional_ai.bat
```

## Install on Windows

```bat
py -3.11 -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip wheel setuptools
pip install -r requirements.txt
```

Install FFmpeg separately and add `C:\ffmpeg\bin` to PATH.

## Run album processing

Put audio files in:

```text
input_album/
```

Run:

```bat
python main.py
```

Output:

```text
output_album/
├── masters/
├── mp3_320/
├── wav/
├── stems/
├── reports/
├── arrangements/
└── album_package.zip
```

## Run MCP/FastAPI server

```bat
run_server.bat
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Prompt Producer example

POST `/music/prompt-producer`

```json
{
  "track_name": "Green Season",
  "prompt": "adicione chuva, pássaros, pianos, violinos, backing vocals e atmosfera Pink Floyd",
  "output_dir": "output_album/arrangements"
}
```
