import torch, os

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

from diffusers import StableDiffusionInpaintPipeline
from PIL import Image

print(torch.cuda.is_available())

pipe = StableDiffusionInpaintPipeline.from_pretrained("stabilityai/stable-diffusion-2-inpainting",torch_dtype=torch.float64)
pipe = pipe.to("cpu")
prompt =  "wall"

image = Image.open("porsche-911.jpg")
mask_image = Image.open("mask.jpg")

#image and mask_image should be PIL images.
#The mask structure is white for inpainting and black for keeping as is
image = pipe(prompt=prompt, image=image, mask_image=mask_image).images[0]
image.save("./image-output.png")