# -*- coding: utf-8 -*-
"""Конвертация Niko_Matrix.png в icon.ico для exe и taskbar"""

try:
    from PIL import Image
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image

import os

def create_icon():
    base = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(base, 'images')
    os.makedirs(img_dir, exist_ok=True)
    png_path = os.path.join(img_dir, 'Niko_Matrix.png')
    ico_path = os.path.join(img_dir, 'icon.ico')
    if os.path.isfile(png_path):
        img = Image.open(png_path).convert('RGBA')
        img.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
        print(f"images/icon.ico created from Niko_Matrix.png")
    else:
        print(f"Warning: {png_path} not found, using fallback")
        w, h = 256, 256
        img = Image.new('RGBA', (w, h), (0, 0, 0, 255))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        for i in range(0, w, 6):
            for j in range(0, h, 10):
                alpha = 120 + (i + j) % 135
                draw.rectangle([i, j, i + 2, j + 5], fill=(0, 255, 0, alpha))
        cx = w // 2 - 4
        for j in range(0, h, 8):
            draw.rectangle([cx, j, cx + 8, j + 10], fill=(0, 255, 120, 255))
        img.save(ico_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
        print("images/icon.ico created (fallback)")

if __name__ == "__main__":
    create_icon()
