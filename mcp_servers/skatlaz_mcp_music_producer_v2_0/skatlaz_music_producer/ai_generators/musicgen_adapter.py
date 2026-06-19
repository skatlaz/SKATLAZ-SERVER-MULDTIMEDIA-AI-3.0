from __future__ import annotations
from pathlib import Path

class MusicGenUnavailable(RuntimeError):
    pass

class MusicGenAdapter:
    """Optional AudioCraft/MusicGen adapter.

    This file is intentionally lazy-loaded so Windows v1/v2 core keeps stable.
    Install optional deps only when needed:
        pip install audiocraft sentencepiece xformers
    """
    def __init__(self, model_name: str = "facebook/musicgen-small"):
        try:
            from audiocraft.models import MusicGen
        except Exception as exc:
            raise MusicGenUnavailable(
                "AudioCraft/MusicGen não está instalado. Instale opcionalmente com: pip install audiocraft sentencepiece"
            ) from exc
        self.model = MusicGen.get_pretrained(model_name)

    def generate_layer(self, prompt: str, output_wav: Path, duration: int = 20) -> Path:
        import torch
        import torchaudio
        output_wav.parent.mkdir(parents=True, exist_ok=True)
        self.model.set_generation_params(duration=duration)
        wav = self.model.generate([prompt])[0].cpu()
        sr = self.model.sample_rate
        if wav.dim() == 1:
            wav = wav.unsqueeze(0)
        torchaudio.save(str(output_wav), wav, sr)
        return output_wav
