from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation
from diffusers import StableDiffusionInpaintPipeline
from PIL import Image
import torch, numpy as np

# Replace a promt from original image with a new prompt
def correction(img_obj, prompt_mask, prompt_inpaint, threshold):

    # Load the CLIPSeg model and processor
    processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
    model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")

    # Load the StableDiffusion model (float32 cost less time than float64 and work on cpu)
    pipeline = StableDiffusionInpaintPipeline.from_pretrained("stabilityai/stable-diffusion-2-inpainting",torch_dtype=torch.float32)

    # Set the device to CPU
    pipeline = pipeline.to("cpu")

    # Give a random number 
    random_number = np.random.randint(0, 1000000000)

    # Load the input image
    image = Image.open(img_obj)

    # Keep the original size of the image
    original_size = image.size

    # Set up the inputs for the model
    inputs = processor(text=[prompt_mask], images=[image] * len([prompt_mask]), padding="max_length", return_tensors="pt")

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

    # Resize the mask and the image to 512x512 needed for the inpainting process 
    # (watch on https://huggingface.co/stabilityai/stable-diffusion-2-inpainting) Training section
    mask_image, image = mask_image.resize((512, 512)), image.resize((512, 512))

    # Inpainting process
    image = pipeline(prompt=prompt_inpaint, image=image, mask_image=mask_image).images[0]

    # Resize the image to the original size
    mask_image, image = mask_image.resize(original_size), image.resize(original_size)
    
    # Set up the filename for the output mask and add a random number
    filename_mask,filename_image = f"mask_"+img_obj.name, f"image_"+img_obj.name

    # Save the mask to a file in JPEG format
    mask_image.save("output/"+filename_mask), image.save("output/"+filename_image)

    return mask_image, image

# Smoke test
#if __name__ == "__main__":
#    correction("porsche-911.jpg", "sponsor", "wall", 0.1)