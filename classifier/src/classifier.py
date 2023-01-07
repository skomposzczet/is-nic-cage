import tensorflow as tf
from tensorflow import keras
from keras import layers
from keras.models import Sequential
from .dataset import Dataset
from os.path import exists


class Classifier:
    def __init__(self):
        print("[CAGE-Classifier] Initializing classifier")
        if not exists("model"):
            self.create_classifier()
        else:
            self.update_classifier()

    def create_classifier(self):
        self.get_dataset()

        self.model = Sequential([
            layers.RandomFlip("horizontal",
                              input_shape=(self.dataset.img_height,
                                           self.dataset.img_width,
                                           3)),
            layers.RandomRotation(0.1),
            layers.Rescaling(
                1./255, input_shape=(self.dataset.img_height, self.dataset.img_width, 3)),
            layers.Conv2D(16, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding='same', activation='relu'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(128, activation='relu'),
            layers.Dense(self.number_of_classes)
        ])

        self.model.compile(optimizer='adam',
                           loss=tf.keras.losses.SparseCategoricalCrossentropy(
                               from_logits=True),
                           metrics=['accuracy'])

        self.model.summary()

    def update_classifier(self):
        self.get_dataset()
        self.model = keras.models.load_model('model')

    def get_dataset(self):
        self.dataset = Dataset()
        self.class_names = self.dataset.class_names
        self.number_of_classes = len(self.class_names)

    def train(self):
        print("[CAGE-Classifier] Training classifier")
        self.epochs = 15
        self.history = self.model.fit(
            self.dataset.training_dataset,
            validation_data=self.dataset.validation_dataset,
            epochs=self.epochs
        )

    def save(self):
        print("[CAGE-Classifier] Saving classifier")
        self.model.save('model')
