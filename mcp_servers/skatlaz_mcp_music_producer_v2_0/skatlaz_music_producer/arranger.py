from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json

@dataclass
class ArrangementLayer:
    name: str
    prompt: str
    start: str = "auto"
    end: str = "auto"
    volume_db: float = -12.0
    pan: str = "center"
    status: str = "planned"  # planned | generated | skipped

@dataclass
class ArrangementPlan:
    track: str
    mood: str
    color: str
    reference: str
    layers: list[ArrangementLayer]

DEFAULT_LAYERS = [
    ArrangementLayer("rain_fx", "soft distant rain, cinematic blues atmosphere", "intro", "outro", -22, "wide"),
    ArrangementLayer("birds_fx", "morning birds in a green forest, subtle and musical", "intro", "verse_1", -24, "wide"),
    ArrangementLayer("bells", "soft tubular bells, vintage progressive rock, emotional accent", "chorus", "bridge", -16, "right"),
    ArrangementLayer("piano", "warm acoustic piano, blues rock ballad, gentle emotional chords", "verse", "full", -10, "left"),
    ArrangementLayer("violins", "soft string section, long notes, emotional crescendo", "pre_chorus", "final", -13, "wide"),
    ArrangementLayer("backing_vocals", "ethereal female backing vocals, ahh and ooh, 70s progressive rock", "chorus", "final", -15, "wide"),
    ArrangementLayer("synth_pad", "analog synth pad, Pink Floyd inspired atmosphere, blue and silver tone", "intro", "full", -18, "wide"),
    ArrangementLayer("extra_guitar", "clean stereo electric guitar, blues phrasing, tape delay", "bridge", "solo", -11, "right"),
]

def make_arrangement_plan(track_name: str, analysis: dict | None = None, style: str = "pink_floyd_blues") -> ArrangementPlan:
    bpm = analysis.get("bpm") if analysis else None
    key = analysis.get("key") if analysis else None
    mood = "cinematic blues progressive"
    color = "deep blue, olive green, silver, vintage gold"
    ref = "Pink Floyd atmosphere, blues rock, Buskplay AI-DSP Press"
    layers = [ArrangementLayer(**asdict(x)) for x in DEFAULT_LAYERS]
    if bpm:
        for layer in layers:
            layer.prompt += f", tempo around {round(float(bpm))} BPM"
    if key:
        for layer in layers:
            layer.prompt += f", compatible with key {key}"
    return ArrangementPlan(track=track_name, mood=mood, color=color, reference=ref, layers=layers)

def save_arrangement_plan(plan: ArrangementPlan, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    safe = Path(plan.track).stem.replace(" ", "_")
    out = output_dir / f"{safe}_arrangement_plan.json"
    data = asdict(plan)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    md = output_dir / f"{safe}_arrangement_plan.md"
    lines = [f"# Arrangement Plan - {plan.track}", "", f"Mood: {plan.mood}", f"Color: {plan.color}", f"Reference: {plan.reference}", "", "## Layers"]
    for layer in plan.layers:
        lines.append(f"- **{layer.name}** [{layer.start} → {layer.end}] {layer.volume_db} dB / {layer.pan}: {layer.prompt}")
    md.write_text("\n".join(lines), encoding="utf-8")
    return out
