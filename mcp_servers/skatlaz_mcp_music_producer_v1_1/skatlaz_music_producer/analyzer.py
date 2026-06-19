from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

import numpy as np
import librosa
import soundfile as sf


KEY_NAMES = [
    "C", "C#/Db", "D", "D#/Eb", "E", "F",
    "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"
]


def dbfs_from_rms(rms: float) -> float:
    if rms <= 0:
        return -120.0
    return float(20.0 * np.log10(rms))


def estimate_key(y: np.ndarray, sr: int) -> str:
    if y.ndim > 1:
        y_mono = librosa.to_mono(y)
    else:
        y_mono = y

    chroma = librosa.feature.chroma_cqt(y=y_mono, sr=sr)
    profile = chroma.mean(axis=1)
    idx = int(np.argmax(profile))
    return KEY_NAMES[idx]


def analyze_audio(file_path: Path) -> Dict[str, Any]:
    y, sr = librosa.load(str(file_path), sr=None, mono=True)
    duration = float(librosa.get_duration(y=y, sr=sr))

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    tempo = float(np.asarray(tempo).reshape(-1)[0])

    rms = float(np.sqrt(np.mean(y ** 2)))
    peak = float(np.max(np.abs(y))) if len(y) else 0.0
    rms_dbfs = dbfs_from_rms(rms)
    peak_dbfs = 20 * np.log10(max(peak, 1e-9))

    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))
    spectral_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
    spectral_rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))

    key = estimate_key(y, sr)

    return {
        "file": file_path.name,
        "sample_rate": sr,
        "duration_seconds": round(duration, 2),
        "tempo_bpm_estimate": round(tempo, 2),
        "key_estimate": key,
        "rms": round(rms, 6),
        "rms_dbfs": round(rms_dbfs, 2),
        "peak": round(peak, 6),
        "peak_dbfs": round(float(peak_dbfs), 2),
        "zero_crossing_rate": round(zcr, 6),
        "spectral_centroid_hz": round(spectral_centroid, 2),
        "spectral_rolloff_hz": round(spectral_rolloff, 2),
        "notes": make_notes(rms_dbfs, peak_dbfs, spectral_centroid),
    }


def make_notes(rms_dbfs: float, peak_dbfs: float, spectral_centroid: float):
    notes = []

    if peak_dbfs >= -0.2:
        notes.append("Peak muito próximo de 0 dBFS; usar limiter com cuidado para evitar clipping.")
    elif peak_dbfs < -6:
        notes.append("Faixa com bastante headroom; pode receber ganho de masterização.")

    if rms_dbfs < -22:
        notes.append("Volume médio baixo; pode ganhar presença e corpo.")
    elif rms_dbfs > -12:
        notes.append("Volume médio alto; preservar dinâmica e evitar compressão excessiva.")

    if spectral_centroid < 1600:
        notes.append("Timbre geral mais escuro; pode aceitar brilho em presença/ar.")
    elif spectral_centroid > 3300:
        notes.append("Timbre brilhante; controlar agudos e sibilância.")

    if not notes:
        notes.append("Faixa equilibrada para masterização leve.")

    return notes
