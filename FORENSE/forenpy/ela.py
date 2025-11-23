from PIL import Image, ImageChops, ImageEnhance
import os

def ela_image(path: str, save_path: str, quality: int = 90, scale: int = 10):
    original = Image.open(path).convert("RGB")
    temp_path = path + ".resaved.jpg"
    original.save(temp_path, 'JPEG', quality=quality)
    resaved = Image.open(temp_path)
    diff = ImageChops.difference(original, resaved)

    extrema = diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    enhancer = ImageEnhance.Brightness(diff)
    ela_img = enhancer.enhance(scale)
    ela_img.save(save_path)
    try:
        os.remove(temp_path)
    except OSError:
        pass
    return save_path
