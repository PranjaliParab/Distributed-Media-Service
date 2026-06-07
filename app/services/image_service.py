import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Output folder
PROCESSED_DIR = "processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)


def resize_image(input_path: str, width: int = 800, height: int = 600) -> str:
    """
    Image resize karato given width x height la.
    """
    img = Image.open(input_path)
    img = img.resize((width, height), Image.LANCZOS)

    filename = Path(input_path).stem + "_resized.jpg"
    output_path = os.path.join(PROCESSED_DIR, filename)
    img.save(output_path, "JPEG")

    print(f"[Image] Resized: {output_path}")
    return output_path


def compress_image(input_path: str, quality: int = 60) -> str:
    """
    Image compress karato — quality 1 (worst) to 95 (best).
    60 he default ahe (file size kam hoto, quality okay rahato).
    """
    img = Image.open(input_path)

    # RGBA asla tar RGB la convert kar (JPEG la alpha channel nako)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    filename = Path(input_path).stem + "_compressed.jpg"
    output_path = os.path.join(PROCESSED_DIR, filename)
    img.save(output_path, "JPEG", quality=quality, optimize=True)

    print(f"[Image] Compressed: {output_path}")
    return output_path


def add_watermark(input_path: str, watermark_text: str = "© My Company") -> str:
    """
    Image var text watermark takto.
    """
    img = Image.open(input_path).convert("RGBA")

    # Watermark layer banav (transparent)
    watermark_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_layer)

    # Font size set kar (default font use karto)
    font_size = max(20, img.width // 20)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Text bottom-right corner la takaycha
    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = img.width - text_width - 20
    y = img.height - text_height - 20

    # Semi-transparent white text
    draw.text((x, y), watermark_text, fill=(255, 255, 255, 180), font=font)

    # Layer merge kar
    watermarked = Image.alpha_composite(img, watermark_layer).convert("RGB")

    filename = Path(input_path).stem + "_watermarked.jpg"
    output_path = os.path.join(PROCESSED_DIR, filename)
    watermarked.save(output_path, "JPEG")

    print(f"[Image] Watermarked: {output_path}")
    return output_path