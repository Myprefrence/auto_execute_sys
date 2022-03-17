import tesserocr
from PIL import Image
import os

img_path=os.path.dirname(os.path.abspath('.')) + '/img/timg.jpg'
print(img_path)

img = Image.open(img_path)

result = tesserocr.image_to_text(img)
print(result)