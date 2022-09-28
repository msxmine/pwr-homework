from PIL import Image
import sys

print(sys.argv[1])
im = Image.open(sys.argv[1]).convert("RGB")
im.save(f"{sys.argv[1]}.tga", compression=None)
