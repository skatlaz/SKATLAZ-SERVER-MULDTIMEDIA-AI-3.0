from dataclasses import dataclass

SUPPORTED_AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"}

@dataclass
class MasterPreset:
    name: str = "Buskplay AI-DSP Press Master"
    target_peak_db: float = -1.0
    bass_gain_db: float = 1.2
    mid_gain_db: float = 0.3
    presence_gain_db: float = 1.0
    air_gain_db: float = 1.4
    compressor_threshold_db: float = -18.0
    compressor_ratio: float = 2.0
    limiter_ceiling_db: float = -1.0
    mp3_bitrate: str = "320k"
