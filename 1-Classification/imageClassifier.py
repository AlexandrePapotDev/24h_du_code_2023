from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import os


id2label = {'0': 'exclure', '1': 'ok', '2': 'retoucher'}

checkpoint = "checkpoint-21"

image_processor = ViTImageProcessor.from_pretrained(checkpoint)

model  = ViTForImageClassification.from_pretrained(checkpoint)

def predictClass(img_path):
    image = Image.open(img_path)
    inputs = image_processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits

    predicted_class_idx = logits.argmax(-1).item()
    #print("Predicted class:", model.config.id2label[predicted_class_idx])

    return model.config.id2label[predicted_class_idx]