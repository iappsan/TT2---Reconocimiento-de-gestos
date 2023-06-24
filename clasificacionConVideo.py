import numpy as np
from keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf
from keras.models import load_model
from time import time
import cv2
from PIL import Image
from numpy import asfarray

batch_size = 32

longitud, altura = 50, 50
modelo = './modelo/modelo.h5'
pesos_modelo = './modelo/pesos.h5'
cnn = load_model(modelo)
cnn.summary()


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
def predict(imagen):
  horaInicio = time()  
  h1 = time()
  result = np.argmax(cnn.predict(imagen) > 0.5).astype("int32")
  print(result)
  #array = cnn.predict_classes(x,1,verbose = 0)
  h2 = time()
  #print(str(h2-h1))
  #answer = np.argmax(result)
  if result == 0:
    print("pred: CincoDedos")
    return "pred: CincoDedos"
  elif result == 1:
    print("pred: Punio")
    return "pred: Punio"
  #horaFinal = time()  
  #print(str(horaFinal - horaInicio))
  

#frame = "C:\\Users\\Oscar\\Documents\\DataSetSoloManos\\Telefono\\4-C-F.jpg"
#x = load_img(frame, target_size=(longitud, altura))
#x = img_to_array(x)
#x = np.expand_dims(x, axis=0)
#print(x)
#print(x[0][0][0][0])
#print(type(x[0][0][0][0]))
#predict(x)


while True:
    ret, frame = cap.read()
    if ret == False:
        break
    height, width, _ = frame.shape
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow('Frame',frame)
    frame2 = frame[0:400,0:400]
    dim = (50, 50)
    # resize image
    resized = cv2.resize(frame2, dim, interpolation = cv2.INTER_AREA)
    #roi = resized.reshape(-1,28,28,1)
    cv2.imshow('Frame2',resized)  
    numpydata = asfarray(resized,dtype='float32')
    x = np.expand_dims(numpydata, axis=0)
    texto = predict(x)
    cv2.putText(frame,texto,(300,100),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
    if cv2.waitKey(1) & 0xFF == 13:
        break


"""

while(True):
    
    ret, frame = cap.read()
    if ret == False:
        break
    frame = cv2.flip(frame,1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #frame2 = frame[100:400,320:620]
    cv2.imshow('frame',frame)
    #frame2 = cv2.resize(frame2,(50,50),interpolation=cv2.INTER_AREA)

    #cv2.imshow('frame2 b/n',frame2)
    #copy = frame.copy()
    #cv2.rectangle(copy,(320,100),(620,400),(255,0,0),5)    
    #frame2 = frame2.reshape(-1,1,50,50)
    #x = load_img(frame2, target_size=(longitud, altura))
    #x = img_to_array(frame2)
    #x = np.expand_dims(x, axis=0)
    #predict(frame2)
    

"""