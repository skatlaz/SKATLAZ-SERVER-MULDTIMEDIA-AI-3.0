from __future__ import annotations

from pathlib import Path
import zipfile


def make_zip(output_dir: Path, zip_path: Path):
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in output_dir.rglob("*"):
            if file.is_file() and file != zip_path:
                zf.write(file, arcname=file.relative_to(output_dir))

    return zip_path
