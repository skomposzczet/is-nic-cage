import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
from classifier.src.detection import detect_face


def check_if_nick(filaneme):
    model = keras.models.load_model('classifier/model')
    img_height = 180
    img_width = 180

    faces = detect_face(filaneme)
    if len(faces) == 0:
        return "No folks on picture"

    for face in faces:
        img_resize = cv2.resize(face, (img_height , img_width ))
        rgb = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)
        rgb_tensor = tf.convert_to_tensor(rgb, dtype=tf.float32)
        img_array = tf.expand_dims(rgb_tensor, 0)
    
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        if np.argmax(score) == 0:
            return "It is Nick ({:.2f}%)".format(100 * np.max(score))

    return "It ain't Nick" 