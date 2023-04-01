from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation
from PIL import Image
import numpy as np
import torch

# Load the CLIPSeg model and processor
processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")

def create_mask(image_path, prompt, threshold=0.5):
    # Load the input image
    image = Image.open(image_path)

    # Define the prompts and set up the inputs for the model
    prompts = [prompt]
    inputs = processor(text=prompts, images=[image] * len(prompts), padding="max_length", return_tensors="pt")

    # Make predictions with the model
    with torch.no_grad():
        outputs = model(**inputs)
    preds = outputs.logits.unsqueeze(0).unsqueeze(1)

    # Compute the segmentation probabilities for the image
    probs = torch.sigmoid(preds[0][0]).cpu().numpy()

    # Threshold the probabilities to obtain the mask
    mask = (probs >= threshold).astype(np.uint8)

    # Resize the mask to match the size of the input image
    mask_image = Image.fromarray(mask * 255).resize(image.size)

    # Set up the filename for the output mask
    filename = f"mask.jpg"

    # Save the mask to a file in JPEG format
    mask_image.save(filename)

    return mask_image

create_mask("image.jpg", "a car").save("mask.jpg")