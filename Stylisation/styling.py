import glob
import numpy as np
from PIL import Image
import tensorflow as tf
# import tensorflow_hub as hub

model = tf.saved_model.load('../models/fnst')
# tf.saved_model.save(style_transfer_model, './models/fnst')


def perform_style_transfer(content_path, style_path, output_path):
    
    content_image = np.array(Image.open(content_path).convert('RGB'))
    style_image = np.array(Image.open(style_path).convert('RGB'))

    content_image = tf.convert_to_tensor(content_image, np.float32)[tf.newaxis, ...] / 255.
    style_image = tf.convert_to_tensor(style_image, np.float32)[tf.newaxis, ...] / 255.
    
    output = model(content_image, style_image)
    stylized_image = output[0]
    
    stylized_image = np.uint8(stylized_image[0] * 255)
    Image.fromarray(stylized_image).save(output_path)


nb_files = len(glob.glob("./output/*"))
output_path = 'output/result'+str(nb_files+1)+'.jpg'

# content_path = 'input/input.jpg'
# style_path = 'input/style_anime.jpg'
# perform_style_transfer(content_path, style_path, output_path)
