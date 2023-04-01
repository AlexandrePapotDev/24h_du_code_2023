from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation
from PIL import Image
import requests
import numpy as np
import torch
from scipy.ndimage import filters

# Load the CLIPSeg model and processor
processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")

# Load the input image
image = Image.open("image.jpg")

# Define the prompts and set up the inputs for the model
prompts = ["car","grass"]
inputs = processor(text=prompts, images=[image] * len(prompts), padding="max_length", return_tensors="pt")

# Make predictions with the model
with torch.no_grad():
    outputs = model(**inputs)
preds = outputs.logits.unsqueeze(1)

# Set the threshold for the mask
threshold = 0.5

# Loop over the images and compute the mask for each one
for i, prompt in enumerate(prompts):
    # Compute the segmentation probabilities for the current image
    probs = torch.sigmoid(preds[i][0]).cpu().numpy()

    # Threshold the probabilities to obtain the mask
    mask = (probs >= threshold).astype(np.uint8)

    # Resize the mask to match the size of the input image
    mask_image = Image.fromarray(mask * 255).resize(image.size)

    # Set up the filename for the output mask
    filename = f"mask_{i}.jpg"

    # Save the mask to a file in JPEG format
    mask_image.save(filename)
