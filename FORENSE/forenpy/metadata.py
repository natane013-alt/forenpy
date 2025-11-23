import hashlib
from PIL import Image
import piexif
import os
import json
from datetime import datetime

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def md5_file(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def extract_exif(path: str) -> dict:
    try:
        exif_dict = piexif.load(path)
        readable = {}
        for ifd in exif_dict:
            if exif_dict[ifd]:
                readable[ifd] = {k.decode('utf-8', 'ignore') if isinstance(k, bytes) else str(k):
                                 (v.decode('utf-8', 'ignore') if isinstance(v, bytes) else v)
                                 for k, v in exif_dict[ifd].items()}
        return readable
    except Exception:
        return {}

def file_report(path: str) -> dict:
    stat = os.stat(path)
    try:
        img = Image.open(path)
        width, height = img.size
    except Exception:
        width = height = None
    return {
        "path": path,
        "sha256": sha256_file(path),
        "md5": md5_file(path),
        "size_bytes": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "width": width,
        "height": height,
        "exif": extract_exif(path)
    }

if __name__ == "__main__":
    import sys
    p = sys.argv[1]
    print(json.dumps(file_report(p), indent=2, ensure_ascii=False))
