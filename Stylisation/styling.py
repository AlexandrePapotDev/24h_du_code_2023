import glob
import numpy as np
from PIL import Image
import tensorflow as tf
import torch


def image_from_prompt(path, prompt):

    pipe = torch.load("../models/text2style.pt")

    image = Image.open(path).convert("RGB")

    max_size = 750
    width, height = image.size
    if width > max_size or height > max_size:
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        new_size = (new_width, new_height)
        image = image.resize(new_size)

    images = pipe(prompt, image=image, num_inference_steps=10, image_guidance_scale=1.5, guidance_scale=2.5).images

    nb_files = len(glob.glob("./output/*"))
    output_path = 'output/result'+str(nb_files+1)+'.jpg'
    images[0].save(output_path)


# image_from_prompt('./examples/input.jpg', 'make the car red')
# tf.saved_model.save(style_transfer_model, './models/fnst')


def perform_style_transfer(content_path, style_path):

    model = tf.saved_model.load('../models/fnst')

    image = Image.open(content_path).convert('RGB')

    max_size = 750
    width, height = image.size
    if width > max_size or height > max_size:
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        new_size = (new_width, new_height)
        image = image.resize(new_size)

    content_image = np.array(image)

    image = Image.open(style_path).convert('RGB')

    max_size = 750
    width, height = image.size
    if width > max_size or height > max_size:
        if width > height:
            new_width = max_size
            new_height = int(height * (max_size / width))
        else:
            new_height = max_size
            new_width = int(width * (max_size / height))
        new_size = (new_width, new_height)
        image = image.resize(new_size)

    style_image = np.array(image)

    content_image = tf.convert_to_tensor(content_image, np.float32)[tf.newaxis, ...] / 255.
    style_image = tf.convert_to_tensor(style_image, np.float32)[tf.newaxis, ...] / 255.
    
    output = model(content_image, style_image)
    stylized_image = output[0]

    nb_files = len(glob.glob("./output/*"))
    output_path = 'output/result'+str(nb_files+1)+'.jpg'

    stylized_image = np.uint8(stylized_image[0] * 255)
    Image.fromarray(stylized_image).save(output_path)


# content_path = 'input/input.jpg'
# style_path = 'input/style_anime.jpg'
# perform_style_transfer(content_path, style_path, output_path)
