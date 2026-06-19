from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
from typing import Optional


COMMON_FFMPEG_PATHS = [
    r"C:\\ffmpeg\\bin\\ffmpeg.exe",
    r"C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe",
    r"C:\\Program Files (x86)\\ffmpeg\\bin\\ffmpeg.exe",
]


@dataclass
class DependencyStatus:
    ffmpeg: Optional[str]
    demucs: Optional[str]

    @property
    def has_ffmpeg(self) -> bool:
        return bool(self.ffmpeg)

    @property
    def has_demucs(self) -> bool:
        return bool(self.demucs)


def find_ffmpeg() -> Optional[str]:
    found = shutil.which("ffmpeg")
    if found:
        return found
    for candidate in COMMON_FFMPEG_PATHS:
        if Path(candidate).exists():
            return candidate
    return None


def find_demucs() -> Optional[str]:
    return shutil.which("demucs")


def check_dependencies() -> DependencyStatus:
    return DependencyStatus(ffmpeg=find_ffmpeg(), demucs=find_demucs())


def print_dependency_report(status: DependencyStatus) -> None:
    print("\n=== Dependências do Skatlaz MCP Music Producer ===")
    print(f"FFmpeg: {'OK - ' + status.ffmpeg if status.ffmpeg else 'NÃO ENCONTRADO'}")
    print(f"Demucs:  {'OK - ' + status.demucs if status.demucs else 'NÃO ENCONTRADO'}")
    if not status.ffmpeg:
        print("\nPara instalar FFmpeg no Windows:")
        print("1) Extraia o FFmpeg em C:\\ffmpeg")
        print("2) Adicione C:\\ffmpeg\\bin ao PATH")
        print("3) Feche e abra o PowerShell")
        print("4) Teste: ffmpeg -version")
    if not status.demucs:
        print("\nPara instalar Demucs no ambiente virtual ativo:")
        print("python -m pip install demucs")
    print("=================================================\n")


def run_command(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, **kwargs)
