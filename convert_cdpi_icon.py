# -*- coding: utf-8 -*-
"""Конвертация CDPIUI.ico в CDPIUI.png (для pygame).
   Сначала ищет CDPIUI.ico в папке; если нет — скачивает с GitHub cdpiui.
"""

import os
import sys

try:
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image

CDPI_ICO_URL = "https://raw.githubusercontent.com/Storik4pro/cdpiui/main/NewSetup/Resources/Icon.ico"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMG_DIR, exist_ok=True)
ICO_PATH = os.path.join(IMG_DIR, "CDPIUI.ico")
PNG_PATH = os.path.join(IMG_DIR, "CDPIUI.png")
SIZE = 128


def convert_ico_to_png(ico_path, png_path, size=SIZE):
    """Конвертирует ICO в PNG с заданным размером."""
    img = Image.open(ico_path)
    img = img.convert("RGBA")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    img.save(png_path, "PNG")
    print(f"Сохранено: {png_path}")


def download_icon():
    """Скачивает иконку с GitHub."""
    try:
        if sys.version_info >= (3, 0):
            from urllib.request import urlretrieve
        else:
            from urllib import urlretrieve
        urlretrieve(CDPI_ICO_URL, ICO_PATH)
        return True
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return False


def main():
    ico_src = ICO_PATH
    if not os.path.isfile(ICO_PATH):
        print("CDPIUI.ico не найден. Загружаю с GitHub...")
        if not download_icon():
            print("Положите CDPIUI.ico в папку images/ и запустите скрипт снова.")
            return 1
    convert_ico_to_png(ico_src, PNG_PATH, SIZE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
