from pathlib import Path

import PIL
import torchvision

basedir = Path(__file__).parent.parent

def load_image(request, reshaped_size=(256,256)):
  filename = request.json["filename"]
  dir_image = str(basedir / "data" / "orijinal" / filename)

  image_obj = PIL.Image.Open(dir_image).convert('RGB')

  image = image_obj.resize(reshaped_size)

  return image, filename

def image_to_tensor(image):

  image_tensor = torchvision.transforms.function.to_tensor(image)
  return image_tensor