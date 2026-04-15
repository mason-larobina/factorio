#!/usr/bin/env python3
"""Generate video thumbnails with a play button overlay."""

import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

MAX_SIZE = 512
VIDEO_EXTS = {".mp4", ".webm", ".mov", ".mkv"}


def get_duration(video: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(video)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def extract_frame(video: Path, seek: float, out: Path):
    subprocess.run(
        ["ffmpeg", "-ss", f"{seek:.2f}", "-i", str(video),
         "-vframes", "1", "-update", "1", str(out), "-y"],
        capture_output=True, check=True,
    )


def add_play_button(img_path: Path):
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size

    # Resize to max MAX_SIZE on longest side
    scale = MAX_SIZE / max(w, h)
    new_w, new_h = int(w * scale), int(h * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    w, h = img.size

    scale = 4
    ow, oh = w * scale, h * scale
    overlay = Image.new("RGBA", (ow, oh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    cx, cy = ow // 2, oh // 2
    r = min(ow, oh) // 5

    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 0, 0, 140))

    tri_w = int(r * 0.7)
    tri_h = int(r * 0.8)
    x_left = cx - tri_w // 3
    x_right = cx + tri_w * 2 // 3
    draw.polygon([
        (x_left, cy - tri_h // 2),
        (x_left, cy + tri_h // 2),
        (x_right, cy),
    ], fill=(255, 255, 255, 235))

    overlay = overlay.resize((w, h), Image.LANCZOS)
    result = Image.alpha_composite(img, overlay).convert("RGB")
    result.save(img_path, "PNG")


def process_video(video: Path):
    thumb = video.with_name(video.stem + "-thumb.png")
    duration = get_duration(video)
    seek = duration * 0.3
    extract_frame(video, seek, thumb)
    add_play_button(thumb)
    print(f"Generated: {thumb}")


def main():
    search_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    videos = [
        p for p in search_dir.rglob("*")
        if p.suffix.lower() in VIDEO_EXTS
        and not any(part.startswith("_") for part in p.parts)
    ]
    if not videos:
        print(f"No video files found in {search_dir}")
        sys.exit(1)
    for video in videos:
        process_video(video)


if __name__ == "__main__":
    main()
