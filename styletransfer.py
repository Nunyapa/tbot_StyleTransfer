import tensorflow_hub as hub
import tensorflow as tf
import random
import numpy as np
import PIL.Image
import time
import functools




class StyleTransfer:
	stdLoadModel = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1'
	def __init__(self):
		self.hub_module = hub.load(self.stdLoadModel)
	
	@staticmethod
	def process(style_image, content_image):
		content_image = self.load_img(content_image)
		style_image = self.load_img(style_image)
		file_name = "img/processed_img_" + str(random.randint(0, 100000000000))
		stylized_image = self.hub_module(tf.constant(content_image), tf.constant(style_image))[0]
		return self.tensor_to_image(stylized_image).save(file_name)

	@staticmethod	
	def tensor_to_image(tensor):
		tensor = tensor*255
		tensor = np.array(tensor, dtype=np.uint8)
		if np.ndim(tensor)>3:
			assert tensor.shape[0] == 1
			tensor = tensor[0]
		return PIL.Image.fromarray(tensor)

	@staticmethod	
	def load_img(img):
		max_dim = 512
		img = tf.image.convert_image_dtype(img, tf.float32)
		shape = tf.cast(tf.shape(img)[:-1], tf.float32)
		long_dim = max(shape)
		scale = max_dim / long_dim
		new_shape = tf.cast(shape * scale, tf.int32)
		img = tf.image.resize(img, new_shape)
		img = img[tf.newaxis, :]
		return img