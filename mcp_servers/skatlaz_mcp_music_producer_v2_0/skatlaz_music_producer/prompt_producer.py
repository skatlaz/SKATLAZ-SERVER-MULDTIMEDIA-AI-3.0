from __future__ import annotations

KEYWORDS = {
    "chuva": "rain_fx",
    "rain": "rain_fx",
    "pássaros": "birds_fx",
    "passaros": "birds_fx",
    "birds": "birds_fx",
    "sinos": "bells",
    "bells": "bells",
    "violino": "violins",
    "violinos": "violins",
    "strings": "violins",
    "piano": "piano",
    "backing": "backing_vocals",
    "vocais": "backing_vocals",
    "synth": "synth_pad",
    "sintetizador": "synth_pad",
    "guitarra": "extra_guitar",
    "guitar": "extra_guitar",
    "pink floyd": "pink_floyd_mode",
    "great gig": "great_gig_color",
}

def parse_music_prompt(prompt: str) -> dict:
    p = prompt.lower()
    layers = []
    modes = []
    for key, value in KEYWORDS.items():
        if key in p:
            if value.endswith("_mode") or value.endswith("_color"):
                modes.append(value)
            elif value not in layers:
                layers.append(value)
    return {
        "raw_prompt": prompt,
        "layers": layers,
        "modes": modes,
        "style": "pink_floyd_blues" if any("pink" in m for m in modes) else "busk_blues",
    }
