from __future__ import annotations

from pathlib import Path

from .deps import find_demucs, run_command


def demucs_available() -> bool:
    return find_demucs() is not None


def separate_stems(input_file: Path, output_dir: Path, model: str = "htdemucs") -> Path:
    demucs = find_demucs()
    if not demucs:
        raise RuntimeError(
            "Demucs não encontrado no ambiente ativo. Instale com: python -m pip install demucs"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [demucs, "-n", model, "-o", str(output_dir), str(input_file)]
    run_command(cmd)
    return output_dir
