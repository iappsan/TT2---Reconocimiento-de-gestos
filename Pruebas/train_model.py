import keras
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
import cv2
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelBinarizer

train = pd.read_csv('csv\sign_mnist_test.csv')
test = pd.read_csv('csv\sign_mnist_train.csv')

# train.head()
# print(train.shape)

labels = train['label'].values
unique_val = np.array(labels)
# print(np.unique(unique_val))

# plt.figure(figsize = (18,8))
# sns.countplot(x =labels)

train.drop('label', axis=1, inplace=True)

images = train.values
images = np.array([np.reshape(i, (28, 28)) for i in images])
images = np.array([i.flatten() for i in images])


label_binrizer = LabelBinarizer()
labels = label_binrizer.fit_transform(labels)

# Inspect an image
# plt.imshow(images[0].reshape(28,28))


# for i in range(0,10):
#     rand = np.random.randint(0, len(images))
#     input_im = images[rand]

#     sample = input_im.reshape(28,28).astype(np.uint8)
#     sample = cv2.resize(sample, None, fx=10, fy=10, interpolation=cv2.INTER_CUBIC)
#     cv2.imshow("sample image", sample)
#     cv2.waitKey(0)

# cv2.destroyAllWindows()

# Split data 
x_train, x_test, y_train, y_test = train_test_split(images, labels, test_size=0.3, random_state=101)


batch_size = 128
num_classes = 24
epochs = 10

# Scale our images
x_train = x_train/255
x_test = x_test/255

# Reshape them into the size requited by TF and Keras
x_train = x_train.reshape(x_train.shape[0], 28,28,1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)

# plt.imshow(x_train[0].reshape(28,28))

# Create CNN Model

model = Sequential()
model.add(Conv2D(64, kernel_size=(3,3), activation = 'relu', input_shape=(28, 28 ,1) ))
model.add(MaxPooling2D(pool_size = (2, 2)))

model.add(Conv2D(64, kernel_size = (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))

model.add(Conv2D(64, kernel_size = (3, 3), activation = 'relu'))
model.add(MaxPooling2D(pool_size = (2, 2)))

model.add(Flatten())
model.add(Dense(128, activation = 'relu'))
model.add(Dropout(0.20))

model.add(Dense(num_classes, activation = 'softmax'))

# Compile the model
model.compile(loss = keras.losses.categorical_crossentropy, 
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])

print(model.summary())

# Train the model
history = model.fit(x_train, y_train, 
                    validation_data = (x_test, y_test), 
                    epochs=epochs, 
                    batch_size=batch_size
                    )

# Save the model
model.save("modeloGestos.h5")
print('Model saved')

# # View our training history graphic
# plt.plot(history.history['accuracy'])
# plt.plot(history.history['val_accuracy'])
# plt.title("Accuracy")
# plt.xlabel('epoch')
# plt.ylabel('accyracy')
# plt.legend(['train', 'test'])
# plt.show()

# Reshape our test data on unseen data
test_labels = test['label']
test.drop('label', axis = 1, inplace = True)

test_images = test.values
test_images = np.array([np.reshape(i, (28, 28)) for i in test_images])
test_images = np.array([i.flatten() for i in test_images])

test_labels = label_binrizer.fit_transform(test_labels)

test_images = test_images.reshape(test_images.shape[0], 28, 28, 1)

print(test_images.shape)

y_pred = model.predict(test_images)
print (y_pred.round())
print (test_labels)

# Get our accuracy score
from sklearn.metrics import accuracy_score
print(accuracy_score(test_labels, y_pred.round()))
