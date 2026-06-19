from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any
import traceback

from tqdm import tqdm

from .config import SUPPORTED_AUDIO_EXTENSIONS, MasterPreset
from .analyzer import analyze_audio
from .mastering import master_to_wav, encode_mp3
from .stems import separate_stems
from .reports import save_track_report, save_album_report
from .exporter import make_zip
from .deps import check_dependencies, print_dependency_report


class MusicProducerPipeline:
    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        album_title: str = "Untitled Album",
        artist: str = "Unknown Artist",
        label: str = "Buskplay AI-DSP Press",
        run_demucs: bool = True,
        export_mp3: bool = True,
        export_wav: bool = True,
        create_zip: bool = True,
    ):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.album_title = album_title
        self.artist = artist
        self.label = label
        self.run_demucs = run_demucs
        self.export_mp3 = export_mp3
        self.export_wav = export_wav
        self.create_zip = create_zip

        self.masters_wav_dir = self.output_dir / "masters_wav"
        self.masters_mp3_dir = self.output_dir / "masters_mp3"
        self.stems_dir = self.output_dir / "stems"
        self.reports_dir = self.output_dir / "reports"

        self.preset = MasterPreset()

    def list_audio_files(self) -> List[Path]:
        if not self.input_dir.exists():
            self.input_dir.mkdir(parents=True, exist_ok=True)

        files = [
            p for p in self.input_dir.iterdir()
            if p.is_file() and p.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS
        ]
        return sorted(files)

    def process_album(self):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        tracks = self.list_audio_files()

        if not tracks:
            print(f"Nenhum áudio encontrado em {self.input_dir.resolve()}")
            print("Coloque arquivos .mp3, .flac ou .wav em input_album/ e rode novamente.")
            return

        album_reports: List[Dict[str, Any]] = []

        deps = check_dependencies()
        print_dependency_report(deps)
        if not deps.has_ffmpeg:
            print("Aviso: masterização/exportação MP3 serão puladas sem FFmpeg.")
            self.export_wav = False
            self.export_mp3 = False
        if self.run_demucs and not deps.has_demucs:
            print("Aviso: separação de stems será pulada sem Demucs.")
            self.run_demucs = False

        print(f"Processando álbum: {self.album_title} - {self.artist}")
        print(f"Faixas encontradas: {len(tracks)}")

        for track in tqdm(tracks, desc="Faixas"):
            try:
                report = analyze_audio(track)
                report["album_title"] = self.album_title
                report["artist"] = self.artist
                report["label"] = self.label

                report["status"] = "analyzed"

                master_wav = self.masters_wav_dir / f"{track.stem}_master.wav"

                if self.export_wav or self.export_mp3:
                    print(f"\nMasterizando: {track.name}")
                    master_to_wav(track, master_wav, self.preset)
                    report["master_wav"] = str(master_wav)
                    report["status"] = "mastered"

                if self.export_mp3:
                    mp3_path = self.masters_mp3_dir / f"{track.stem}_master.mp3"
                    encode_mp3(master_wav, mp3_path, self.preset.mp3_bitrate)
                    report["master_mp3"] = str(mp3_path)

                if self.run_demucs:
                    print(f"Separando stems: {track.name}")
                    separate_stems(track, self.stems_dir)
                    report["stems"] = str(self.stems_dir)

                save_track_report(report, self.reports_dir)
                album_reports.append(report)

            except Exception as exc:
                error_report = {
                    "file": track.name,
                    "status": "error",
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                    "duration_seconds": 0,
                    "tempo_bpm_estimate": "N/A",
                    "key_estimate": "N/A",
                    "rms_dbfs": "N/A",
                    "peak_dbfs": "N/A",
                    "notes": ["A faixa falhou, mas o pipeline continuou para as próximas músicas."],
                }
                save_track_report(error_report, self.reports_dir)
                album_reports.append(error_report)
                print(f"Erro ao processar {track.name}: {exc}")

        album_report = {
            "album_title": self.album_title,
            "artist": self.artist,
            "label": self.label,
            "tracks": album_reports,
            "version": "Skatlaz MCP Music Producer 1.1",
        }
        save_album_report(album_report, self.reports_dir)

        if self.create_zip:
            zip_path = self.output_dir / "album_package.zip"
            make_zip(self.output_dir, zip_path)
            print(f"\nZIP final criado: {zip_path.resolve()}")

        print("\nProcesso finalizado.")
