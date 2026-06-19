from pathlib import Path


def seconds_to_srt_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def create_srt(lines: list[str], output_path: str, seconds_per_line: int = 4) -> str:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    chunks = []
    for i, line in enumerate(lines, start=1):
        start = (i - 1) * seconds_per_line
        end = i * seconds_per_line
        chunks.append(f"{i}\n{seconds_to_srt_time(start)} --> {seconds_to_srt_time(end)}\n{line}\n")
    Path(output_path).write_text("\n".join(chunks), encoding='utf-8')
    return output_path
