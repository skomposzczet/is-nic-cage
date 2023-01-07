import os
import cv2
import tensorflow as tf
from .detection import detect_face


class Dataset:
    def __init__(self):
        print("[CAGE-Classifier] Initializing dataset")
        self.init_params()
        self.prepare_dataset()
        self.create_dataset()

    def init_params(self):
        self.data_path = "pictures"

        self.batch_size = 32
        self.img_height = 180
        self.img_width = 180

        self.validation_split = 0.1

    def prepare_dataset(self):
        self.prepare_nick_data()
        self.prepare_others_data()

    def prepare_nick_data(self):
        print("[CAGE-Classifier] Prepare Nick data")
        nick_data_path = os.path.join(self.data_path, "nick")

        for filename in os.listdir(nick_data_path):
            image_path = os.path.join(nick_data_path, filename)
            faces = detect_face(image_path)
            os.remove(image_path)

            print("[CAGE-Classifier] Process {} image".format(image_path))

            # Saving only photos of nick cage without other folks
            if len(faces) == 1:
                cv2.imwrite(image_path, faces[0])

    def prepare_others_data(self):
        print("[CAGE-Classifier] Prepare others data")
        others_data_path = os.path.join(self.data_path, "others")

        for filename in os.listdir(others_data_path):
            image_path = os.path.join(others_data_path, filename)
            faces = detect_face(image_path)
            os.remove(image_path)

            print("[CAGE-Classifier] Process {} image".format(image_path))

            for index, face in enumerate(faces):
                new_image_path = os.path.splitext(
                    image_path)[0] + str(index) + os.path.splitext(image_path)[1]
                cv2.imwrite(new_image_path, face)

    def create_dataset(self):
        self.autotune = tf.data.AUTOTUNE
        self.create_training_dataset()
        self.create_validation_dataset()

    def create_training_dataset(self):
        print("[CAGE-Classifier] Creating training dataset")
        training_dataset = tf.keras.utils.image_dataset_from_directory(
            self.data_path,
            validation_split=self.validation_split,
            subset="training",
            seed=123,
            image_size=(self.img_height, self.img_width),
            batch_size=self.batch_size)

        self.training_dataset = training_dataset.cache().shuffle(
            1000).prefetch(buffer_size=self.autotune)

        self.class_names = training_dataset.class_names

    def create_validation_dataset(self):
        print("[CAGE-Classifier] Creating validation dataset")
        validation_dataset = tf.keras.utils.image_dataset_from_directory(
            self.data_path,
            validation_split=self.validation_split,
            subset="validation",
            seed=123,
            image_size=(self.img_height, self.img_width),
            batch_size=self.batch_size)

        self.validation_dataset = validation_dataset.cache().prefetch(
            buffer_size=self.autotune)
