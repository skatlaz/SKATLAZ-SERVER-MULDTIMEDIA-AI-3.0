from __future__ import annotations

from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel

from skatlaz_music_producer.pipeline import MusicProducerPipeline
from skatlaz_music_producer.prompt_producer import parse_music_prompt
from skatlaz_music_producer.arranger import make_arrangement_plan, save_arrangement_plan

app = FastAPI(
    title="Skatlaz MCP Music Producer 2.0",
    description="Prompt-based MCP music producer server for Buskplay AI-DSP Press and Skatlaz Server AI.",
    version="2.0.0",
)

class AlbumJob(BaseModel):
    input_dir: str = "input_album"
    output_dir: str = "output_album"
    album_title: str = "My Damn Blues Book"
    artist: str = "Busk Blues"
    label: str = "Buskplay AI-DSP Press"
    run_demucs: bool = True

class PromptJob(BaseModel):
    prompt: str
    track_name: str = "album"
    output_dir: str = "output_album/arrangements"

@app.get("/")
def index():
    return {
        "name": "Skatlaz MCP Music Producer",
        "version": "2.0.0",
        "tools": [
            "music.process_album",
            "music.prompt_producer",
            "music.make_arrangement_plan",
            "music.generate_optional_layer",
            "music.export_album_zip",
        ],
        "note": "MusicGen/AudioCraft are optional in v2.0 and disabled unless installed.",
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
    return {"status": "done", "output_dir": job.output_dir, "zip": f"{job.output_dir}/album_package.zip"}

@app.post("/music/prompt-producer")
def prompt_producer(job: PromptJob):
    parsed = parse_music_prompt(job.prompt)
    plan = make_arrangement_plan(job.track_name, analysis=None, style=parsed["style"])
    # keep only requested layers when possible
    if parsed["layers"]:
        plan.layers = [layer for layer in plan.layers if layer.name in parsed["layers"]]
    out = save_arrangement_plan(plan, Path(job.output_dir))
    return {"status": "planned", "parsed": parsed, "plan_json": str(out)}

@app.post("/music/make-arrangement-plan")
def arrangement_plan(job: PromptJob):
    parsed = parse_music_prompt(job.prompt)
    plan = make_arrangement_plan(job.track_name, analysis=None, style=parsed["style"])
    out = save_arrangement_plan(plan, Path(job.output_dir))
    return {"status": "done", "plan_json": str(out), "parsed": parsed}
