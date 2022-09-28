import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

mydataset = open("./mydata/mydataset.npy", "rb")
mydata = np.load(mydataset)
mylabels = np.load(mydataset)
mydataset.close()

mydata = mydata / 255.0

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
model.load_weights(checkpoint_path)

model.evaluate(mydata, mylabels)

mismatchedexamples = []

for i in range(len(mylabels)):
    prediction = np.argmax(tf.nn.softmax(model(mydata[i:i+1])).numpy())
    actual = mylabels[i]
    if actual != prediction:
        mismatchedexamples.append(((mydata[i] * 255.0).astype(int), actual, prediction))

mismatcharr = np.zeros((10,10), dtype=int)
for mismatch in mismatchedexamples:
    mismatcharr[mismatch[1]][mismatch[2]] += 1

print(mismatcharr)

for i in range(len(mismatchedexamples)):
    index = i
    plt.imshow(mismatchedexamples[index][0], cmap="gray_r", vmin=0, vmax=255)
    plt.title("real=" + str(mismatchedexamples[index][1]) + " predicted=" + str(mismatchedexamples[index][2]))
    plt.show()
    #plt.savefig("./errors/my" + str(i) + ".png")

for i in range(len(mismatcharr)):
    realdig = i
    for j in range(len(mismatcharr[i])):
        predicteddig = j
        print(mismatcharr[i][j], ",", end="")
    print("")
