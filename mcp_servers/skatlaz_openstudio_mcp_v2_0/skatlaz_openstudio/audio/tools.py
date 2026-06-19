from pathlib import Path
from pydub import AudioSegment, effects


def audio_info(path: str) -> dict:
    audio = AudioSegment.from_file(path)
    return {
        "file": path,
        "duration_seconds": round(len(audio) / 1000, 2),
        "channels": audio.channels,
        "frame_rate": audio.frame_rate,
        "sample_width": audio.sample_width,
        "max_dBFS": audio.max_dBFS,
        "dBFS": audio.dBFS,
    }


def apply_audio_effects(input_path: str, output_path: str, normalize=True, fade_ms=0, gain_db=0, format=None) -> str:
    audio = AudioSegment.from_file(input_path)
    if normalize:
        audio = effects.normalize(audio)
    if gain_db:
        audio = audio + gain_db
    if fade_ms:
        audio = audio.fade_in(fade_ms).fade_out(fade_ms)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    audio.export(output_path, format=format or Path(output_path).suffix.replace('.', '') or 'mp3')
    return output_path


def add_soundtrack(video_audio_path: str, soundtrack_path: str, output_path: str, soundtrack_gain_db=-10) -> str:
    base = AudioSegment.from_file(video_audio_path)
    track = AudioSegment.from_file(soundtrack_path) + soundtrack_gain_db
    if len(track) < len(base):
        loops = (len(base) // len(track)) + 1
        track = track * loops
    mixed = base.overlay(track[:len(base)])
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    mixed.export(output_path, format=Path(output_path).suffix.replace('.', '') or 'mp3')
    return output_path
