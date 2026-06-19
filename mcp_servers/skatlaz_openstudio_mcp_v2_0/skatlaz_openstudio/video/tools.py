from pathlib import Path


def video_info(path: str) -> dict:
    try:
        from moviepy.editor import VideoFileClip
        clip = VideoFileClip(path)
        info = {"file": path, "duration": clip.duration, "fps": clip.fps, "size": clip.size}
        clip.close()
        return info
    except Exception as e:
        return {"file": path, "error": str(e)}


def apply_video_filter(input_path: str, output_path: str, filter_name: str = 'gray') -> str:
    from moviepy.editor import VideoFileClip
    import moviepy.video.fx.all as vfx
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    clip = VideoFileClip(input_path)
    if filter_name == 'gray':
        clip = clip.fx(vfx.blackwhite)
    elif filter_name == 'mirror':
        clip = clip.fx(vfx.mirror_x)
    elif filter_name == 'speed2x':
        clip = clip.fx(vfx.speedx, 2)
    clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
    clip.close()
    return output_path


def create_thumbnail(input_path: str, output_path: str, time_sec: float = 1.0) -> str:
    from moviepy.editor import VideoFileClip
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    clip = VideoFileClip(input_path)
    frame = clip.get_frame(min(time_sec, max(0, clip.duration-0.1)))
    from PIL import Image
    Image.fromarray(frame).save(output_path)
    clip.close()
    return output_path
