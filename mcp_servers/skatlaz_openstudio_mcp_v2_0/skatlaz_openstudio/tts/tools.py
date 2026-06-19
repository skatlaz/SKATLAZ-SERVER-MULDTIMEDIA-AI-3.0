from pathlib import Path
from gtts import gTTS


def text_to_speech(text: str, output_path: str, lang: str = 'pt') -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    tts = gTTS(text=text, lang=lang)
    tts.save(output_path)
    return output_path
