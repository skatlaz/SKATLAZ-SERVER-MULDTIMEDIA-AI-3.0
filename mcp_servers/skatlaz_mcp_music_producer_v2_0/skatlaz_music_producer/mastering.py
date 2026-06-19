from __future__ import annotations

from pathlib import Path

from .config import MasterPreset
from .deps import find_ffmpeg, run_command


def require_ffmpeg() -> str:
    ffmpeg = find_ffmpeg()
    if not ffmpeg:
        raise RuntimeError(
            "FFmpeg não encontrado. Instale em C:\\ffmpeg\\bin ou adicione ffmpeg ao PATH. "
            "Teste no PowerShell: ffmpeg -version"
        )
    return ffmpeg


def build_master_filter(preset: MasterPreset) -> str:
    return ",".join([
        f"equalizer=f=80:t=q:w=0.8:g={preset.bass_gain_db}",
        f"equalizer=f=900:t=q:w=1.0:g={preset.mid_gain_db}",
        f"equalizer=f=4500:t=q:w=1.0:g={preset.presence_gain_db}",
        f"equalizer=f=12000:t=q:w=0.8:g={preset.air_gain_db}",
        f"acompressor=threshold={preset.compressor_threshold_db}dB:ratio={preset.compressor_ratio}:attack=30:release=180:makeup=1",
        f"alimiter=limit={db_to_linear(preset.limiter_ceiling_db)}",
        "loudnorm=I=-14:TP=-1.0:LRA=11",
    ])


def db_to_linear(db: float) -> float:
    return 10 ** (db / 20)


def master_to_wav(input_file: Path, output_file: Path, preset: MasterPreset):
    ffmpeg = require_ffmpeg()
    output_file.parent.mkdir(parents=True, exist_ok=True)
    filters = build_master_filter(preset)

    cmd = [
        ffmpeg, "-y",
        "-i", str(input_file),
        "-af", filters,
        "-ar", "44100",
        "-ac", "2",
        "-sample_fmt", "s16",
        str(output_file),
    ]
    run_command(cmd)


def encode_mp3(input_file: Path, output_file: Path, bitrate: str = "320k"):
    ffmpeg = require_ffmpeg()
    output_file.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg, "-y",
        "-i", str(input_file),
        "-codec:a", "libmp3lame",
        "-b:a", bitrate,
        str(output_file),
    ]
    run_command(cmd)
