from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import os
from sklearn.metrics import accuracy_score


id2label = {'0': 'exclure', '1': 'ok', '2': 'retoucher'}

label2id = {'exclure': '0', 'ok': '1', 'retoucher': '2'}

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

def evaluate_classifier(input_directory):
    predictions = []
    labels = []

    for dir in os.listdir(input_directory):
        # print(dir)
        if dir in ['exclure', 'ok', 'retoucher']:
            # print(len(dir))
            # print(dir)
            for image in os.listdir(f'{input_directory}/{dir}'):
                if image.split('.')[1] == 'jpg' or image.split('.')[1] == 'png':
                    predicted_class_idx = int(label2id[predictClass(f'{input_directory}/{dir}/{image}')])

                    #image = Image.open(f'{input_directory}/{dir}/{image}')
                    #inputs = image_processor(images=image, return_tensors="pt")
                    #outputs = model(**inputs)
                    #logits = outputs.logits
                    #predicted_class_idx = logits.argmax(-1).item()
                    predictions.append(predicted_class_idx)
                    labels.append(int(label2id[dir]))
                    #print("Predicted class:", model.config.id2label[predicted_class_idx])
    accuracy = accuracy_score(predictions, labels)
    return accuracy
