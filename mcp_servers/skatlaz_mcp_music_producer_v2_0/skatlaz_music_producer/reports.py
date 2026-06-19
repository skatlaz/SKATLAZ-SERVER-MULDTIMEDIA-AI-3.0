from __future__ import annotations

from pathlib import Path
from typing import Dict, Any
import json


def _safe(report: Dict[str, Any], key: str, default: Any = "N/A") -> Any:
    return report.get(key, default)


def save_track_report(report: Dict[str, Any], reports_dir: Path):
    reports_dir.mkdir(parents=True, exist_ok=True)
    filename = str(report.get("file") or report.get("track") or "track_report")
    stem = Path(filename).stem
    json_path = reports_dir / f"{stem}.json"
    txt_path = reports_dir / f"{stem}.txt"

    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        f"Arquivo: {filename}",
        f"Status: {_safe(report, 'status', 'ok')}",
        f"Duração: {_safe(report, 'duration_seconds', 0)}s",
        f"BPM estimado: {_safe(report, 'tempo_bpm_estimate')}",
        f"Tom estimado: {_safe(report, 'key_estimate')}",
        f"RMS: {_safe(report, 'rms_dbfs')} dBFS",
        f"Peak: {_safe(report, 'peak_dbfs')} dBFS",
    ]

    if report.get("error"):
        lines.extend(["", "Erro:", str(report.get("error"))])

    lines.extend(["", "Notas de produção:"])
    for note in report.get("notes", []):
        lines.append(f"- {note}")

    txt_path.write_text("\n".join(lines), encoding="utf-8")


def save_album_report(album_report: Dict[str, Any], reports_dir: Path):
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / "album_report.json"
    path.write_text(json.dumps(album_report, indent=2, ensure_ascii=False), encoding="utf-8")

    txt = reports_dir / "album_report.txt"
    lines = [
        f"Álbum: {album_report.get('album_title')}",
        f"Artista: {album_report.get('artist')}",
        f"Selo: {album_report.get('label')}",
        f"Versão: {album_report.get('version')}",
        "",
        "Faixas:",
    ]

    for item in album_report.get("tracks", []):
        status = item.get("status", "ok")
        if item.get("error"):
            lines.append(f"- {item.get('file')} | ERRO | {item.get('error')}")
        else:
            lines.append(
                f"- {item.get('file')} | {status} | BPM {item.get('tempo_bpm_estimate', 'N/A')} | "
                f"Tom {item.get('key_estimate', 'N/A')} | RMS {item.get('rms_dbfs', 'N/A')} dBFS"
            )

    txt.write_text("\n".join(lines), encoding="utf-8")
