from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from skatlaz_music_producer.pipeline import MusicProducerPipeline

app = FastAPI(
    title="Skatlaz MCP Music Producer 1.0",
    description="MCP-ready music producer server for Buskplay AI-DSP Press and Skatlaz Server AI.",
    version="1.0.0",
)


class AlbumJob(BaseModel):
    input_dir: str = "input_album"
    output_dir: str = "output_album"
    album_title: str = "My Damn Blues Book"
    artist: str = "Busk Blues"
    label: str = "Buskplay AI-DSP Press"
    run_demucs: bool = True


@app.get("/")
def index():
    return {
        "name": "Skatlaz MCP Music Producer",
        "version": "1.0.0",
        "tools": [
            "analyze_album",
            "separate_stems",
            "master_album",
            "export_album_zip",
        ],
    }


@app.post("/music/process-album")
def process_album(job: AlbumJob):
    pipeline = MusicProducerPipeline(
        input_dir=job.input_dir,
        output_dir=job.output_dir,
        album_title=job.album_title,
        artist=job.artist,
        label=job.label,
        run_demucs=job.run_demucs,
        export_mp3=True,
        export_wav=True,
        create_zip=True,
    )
    pipeline.process_album()
    return {
        "status": "done",
        "output_dir": job.output_dir,
        "zip": f"{job.output_dir}/album_package.zip",
    }
