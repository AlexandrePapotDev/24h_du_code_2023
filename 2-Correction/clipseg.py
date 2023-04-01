from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation

processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")

from PIL import Image
import requests
import numpy as np

image = Image.open("image.jpg")
image

prompts = ["car","grass"]

import torch

inputs = processor(text=prompts, images=[image] * len(prompts), padding="max_length", return_tensors="pt")
# predict
with torch.no_grad():
  outputs = model(**inputs)
preds = outputs.logits.unsqueeze(1)

import matplotlib.pyplot as plt

for i, prompt in enumerate(prompts):
    # Convert the image data to a PIL Image object
    image_data = torch.sigmoid(preds[i][0]).cpu().numpy() * 255
    image_data = image_data.astype(np.uint8)
    image = Image.fromarray(image_data)

    # Set up the filename for the output image
    filename = f"output_{i}.jpg"

    # Save the image to a file in JPEG format
    image.save(filename)