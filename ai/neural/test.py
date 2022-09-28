import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(256, (5,5), activation="relu", input_shape=(28,28,1)),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(10)
])

checkpoint_path = "training_1/cp.ckpt"
model.load_weights(checkpoint_path).expect_partial()

im = Image.open("./2.png").convert("L")
myimage = np.array([(255 - np.array(im)) / 255.0])
print(tf.nn.softmax(model(myimage)).numpy())
