import tensorflow as tf

(data_train, labels_train), (data_test, labels_test) = tf.keras.datasets.mnist.load_data()
data_train, data_test = data_train / 255.0, data_test / 255.0

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

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
optimizer_fn = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.1)
model.compile(optimizer=optimizer_fn, loss=loss_fn, metrics=['accuracy'])

checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = "training_1"
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, verbose=1)

model.fit(data_train, labels_train, epochs=15, validation_data=(data_test, labels_test), callbacks=[cp_callback])
