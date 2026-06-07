import os
import ffmpeg
from pathlib import Path

PROCESSED_DIR = "processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)


def compress_video(input_path: str, output_format: str = "mp4") -> str:
    """
    Video compress karato MP4/H.264 format madhe.
    crf = quality (18 best, 28 small size) — 23 default ahe.
    """
    filename = Path(input_path).stem + "_compressed." + output_format
    output_path = os.path.join(PROCESSED_DIR, filename)

    (
        ffmpeg
        .input(input_path)
        .output(
            output_path,
            vcodec="libx264",   # H.264 codec
            crf=23,             # Compression level
            preset="fast",      # Encoding speed
            acodec="aac",       # Audio codec
            audio_bitrate="128k"
        )
        .overwrite_output()
        .run(quiet=True)
    )

    print(f"[Video] Compressed: {output_path}")
    return output_path


def generate_thumbnail(input_path: str, timestamp: str = "00:00:03") -> str:
    """
    Video madhe dilelja timestamp var ek screenshot (thumbnail) kadhto.
    timestamp format: "HH:MM:SS"
    """
    filename = Path(input_path).stem + "_thumbnail.jpg"
    output_path = os.path.join(PROCESSED_DIR, filename)

    (
        ffmpeg
        .input(input_path, ss=timestamp)   # ss = seek to timestamp
        .output(output_path, vframes=1)    # Ek frame kadh
        .overwrite_output()
        .run(quiet=True)
    )

    print(f"[Video] Thumbnail: {output_path}")
    return output_path