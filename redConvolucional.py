import matplotlib.pyplot as plt
import os
import numpy as np

import tensorflow as tf
#from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras import optimizers
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dropout, Flatten, Dense, Activation
from tensorflow.python.keras.layers import  Convolution2D, MaxPooling2D
from tensorflow.python.keras import backend as K
from keras.preprocessing.image import load_img, img_to_array
from time import time

K.clear_session()



data_entrenamiento = 'C:\\Users\\Oscar\\Documents\\TTII\\TensorFlow\\Entrenamiento'
data_validacion = 'C:\\Users\\Oscar\\Documents\\TTII\\TensorFlow\\Validacion'

"""
Parameters
"""
epocas= 150
longitud, altura = 50, 50
batch_size = 32
pasos = 10
validation_steps = 80
filtrosConv1 = 16
filtrosConv2 = 32
tamano_filtro1 = (3, 3)
tamano_filtro2 = (2, 2)
tamano_pool = (2, 2)
clases = 2
lr = 0.0005


##Preparamos nuestras imagenes

entrenamiento_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255)

entrenamiento_generador = entrenamiento_datagen.flow_from_directory(
    data_entrenamiento,
    target_size=(altura, longitud),
    batch_size=batch_size,
    class_mode='categorical')

validacion_generador = test_datagen.flow_from_directory(
    data_validacion,
    target_size=(altura, longitud),
    batch_size=batch_size,
    class_mode='categorical')

cnn = Sequential()
cnn.add(Convolution2D(filtrosConv1, tamano_filtro1, padding ="same", input_shape=(longitud, altura, 3), activation='relu'))
cnn.add(MaxPooling2D(pool_size=tamano_pool))

cnn.add(Convolution2D(filtrosConv2, tamano_filtro2, padding ="same"))
cnn.add(MaxPooling2D(pool_size=tamano_pool))

cnn.add(Flatten())
cnn.add(Dense(64, activation='relu'))
cnn.add(Dropout(0.5))
cnn.add(Dense(clases, activation='softmax'))
#tf.config.optimizer.set_jit(False)
cnn.compile(loss='categorical_crossentropy',
            optimizer="adam",
            metrics=['accuracy'])




history = cnn.fit_generator(
    entrenamiento_generador,
    steps_per_epoch=pasos,
    epochs=epocas,
    validation_data=validacion_generador,
    validation_steps=validation_steps)

target_dir = './modelo/'
if not os.path.exists(target_dir):
  os.mkdir(target_dir)
cnn.save('./modelo/modelo.h5')
cnn.save_weights('./modelo/pesos.h5')

print("hecho")
plt.plot(history.history['accuracy'], label='Exactitud')
plt.plot(history.history['loss'], label = 'Perdida')
plt.xlabel('Épocas')
plt.ylabel('Porcentaje')
plt.ylim([0.1, 1])
plt.legend(loc='lower right')
plt.show()

test_loss, test_acc = cnn.evaluate(validacion_generador, verbose=1)


file="C:\\Users\\Oscar\\Documents\\DataSetSoloManos\\Punio\\0-C-F.jpg"
x = load_img(file, target_size=(longitud, altura))
x = img_to_array(x)
x = np.expand_dims(x, axis=0)
h1 = time()
array = cnn.predict(x)
h2 = time()
print(str(h2-h1))
result = array[0]
answer = np.argmax(result)
if answer == 0:
  print("pred: CincoDedos")
elif answer == 1:
  print("pred: Punio")
horaFinal = time()  
