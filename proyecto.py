import cv2
import numpy as np
import keras
import mediapipe as mp
import threading
import time
from pynput.keyboard import Key, Controller
from escenario import Scene
from numpy import asfarray
from win32api import GetSystemMetrics

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
y = 0
x = 0
timeInSecs = 0
gestureSec = 0
lastGesture = ''
lastGesture2 = 0
keepOpen = True
currentScene = Scene()

#   Convertimos los booleanos en una cadena simple para ejemplificar los gestos
def arrayConv(array) -> str:        
    resultStr = ''
    for i in range(5):
        if(array[i]):
            resultStr = resultStr + '1'
        else:
            resultStr = resultStr + '0'
    # print (resultStr)
    return resultStr

def secVal(actualGesture: str):      # Validamos que el gesto dure 3 segundos por medio de un contador y cuando pase, ejecutamos la accion
    global lastGesture
    global gestureSec
    global keepOpen
    global currentScene

    if lastGesture != actualGesture:
        lastGesture = actualGesture
        gestureSec = timeInSecs
    else:
        if timeInSecs == (gestureSec + 3):
            currentScene.overlayStuff[0] = 'Reconociendo gesto: '+str(actualGesture)
            gestNUM = currentScene.invokeAction(actualGesture)
            if not gestNUM:
                keepOpen = False
                lastGesture = ''
            elif gestNUM < 10:
                print('Ejecutando gesto '+ str(gestNUM-1))
                currentScene.execAct(gestNUM)
            else:
                currentScene.overlayStuff[0] = 'Este gesto no se acepta'
            gestureSec = 0      # Reiniciamos el contador para que solo se ejecute una vez la accion
     
def secVal2(actualGesture: int):      # Validamos que el gesto dure 3 segundos por medio de un contador y cuando pase, ejecutamos la accion
    global lastGesture            # Funcion unicamente para equivalencia del metodo con red neuronal
    global gestureSec
    global keepOpen
    global currentScene

    def equiv(n):
        m = 10
        if n == 0:
            m = 1
        elif n == 3:
            m = 2
        elif n == 20:
            m = 3
        elif n == 5:
            m = 4
        elif n == 1:
            m = 5
        ## AQUI Falta gesto 5
        elif n == 10:
            m = 7
        elif n == 23:
            m = 8
        ## AQUI falta gesto 8
        return m

    if lastGesture != actualGesture:
        lastGesture = actualGesture
        gestureSec = timeInSecs
    else:
        if timeInSecs == (gestureSec + 3):
            currentScene.overlayStuff[0] = 'Reconociendo gesto: '+str(actualGesture)
            gestName = actualGesture
            if actualGesture == 0:
                keepOpen = False
                lastGesture2 = 0
            elif equiv(actualGesture) < 10:
                print(gestName)
                currentScene.execAct(1)
            else:
                currentScene.overlayStuff[0] = 'Este gesto no se acepta'
            gestureSec = 0      # Reiniciamos el contador para que solo se ejecute una vez la accion
     
def secVal3(actualGesture: str):      # Validamos que el gesto dure 3 segundos por medio de un contador y cuando pase, ejecutamos la accion
    global lastGesture                # Funcion unicamente para equivalencia del metodo con red neuronal
    global gestureSec
    global keepOpen
    global currentScene

    def equiv(gesto):
        m = 10
        if gesto == "CincoDedos":
            pass
        elif gesto == "Punio":
            pass


    if lastGesture != actualGesture:
        lastGesture = actualGesture
        gestureSec = timeInSecs
    else:
        if timeInSecs == (gestureSec + 3):
            currentScene.overlayStuff[0] = 'Reconociendo gesto: '+str(actualGesture)
            lastGesture = ''
            if actualGesture == "CincoDedos":
                keepOpen = False
            elif actualGesture == "Punio":
                currentScene.execAct(1)
            else:           #No hay gesto
                pass
            gestureSec = 0      # Reiniciamos el contador para que solo se ejecute una vez la accion
     

# Esta funcion hace una comparacion por diferencia para saber si un dedo esta abierto o no
def openOrNot(WRIST, FT, FB):
    global y
    global x
    wristVector = np.array([WRIST[0], WRIST[1]])
    fingerTipVector = np.array([x*FT.x, y*FT.y])
    fingerBaseVector = np.array([x*FB.x, y*FB.y])

    # Las siguientes dos lineas operan los vectores para calcular la diferencia
    # entre FT (punta del dedo) hacia FB (base del dedo)
    diffFT = np.linalg.norm(wristVector-fingerTipVector)
    diffFB = np.linalg.norm(wristVector-fingerBaseVector)
    # print ('Distance: {}\n'.format(diffFT - diffFB))

    if diffFT-diffFB>0:
        return True
    else:
        return False    
    
def clock():        # Esta funcion nace como un hilo para llevar un conteo de segundos y un registro
    global timeInSecs       # del ultimo gesto registrado
    global lastGesture
    global keepOpen
    while True:
        print('Segundo {}, gesto {}'.format(timeInSecs, lastGesture))
        timeInSecs = timeInSecs +1
        time.sleep(1)
        if not keepOpen:
            print ('Fin de reconocimiento')
            break

def init(cScene: Scene):

    global x
    global y
    global lastGesture
    global keepOpen
    global currentScene

    currentScene = cScene

    timer = threading.Thread(target=clock)
    timer.start()

    # Obtenemos la entrada de la camara
    cap = cv2.VideoCapture(0)

    # Aqui obtenemos el tamano de X y Y
    x = int (cap.get(3))
    y = int (cap.get(4))
    print('x: {}, y {}'.format(x,y))

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        while cap.isOpened() and keepOpen:
            success, image = cap.read()
            cv2.putText(image, 
                str(currentScene.overlayStuff[0]), 
                (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX,1, 
                (0, 255, 255), 
                2, 
                cv2.LINE_4)
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
        
                    # Creamos un punto que indique el centro de la palma
                    wristP = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    midFB = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                    newCx = int((x*wristP.x + x*midFB.x)/2)
                    newCy = int((y*wristP.y + y*midFB.y)/2)
                    cv2.circle(image, (newCx,newCy), 3, (100,33,200),2)  
                    middlePoint = [newCx,newCy]
                    # Creamos un nuevo punto para utilizarlo con el pulgar
                    indFB = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                    thumbFB = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
                    newCx4T = int((x*thumbFB.x + x*1.1*indFB.x)/2)
                    newCy4T = int((y*thumbFB.y + y*.9*indFB.y)/2)
                    # newCx4T = int(((2*x*wristP.x/3) + x*indFB.x)/2)
                    # newCy4T = int(((2*y*wristP.y/3) + y*indFB.y)/2)
                    cv2.circle(image, (newCx4T,newCy4T), 3, (10,150,200),2)
                    thumbPoint = [newCx4T,newCy4T]

                    fingersOpen = []
                    fingersOpen.append(openOrNot(
                        thumbPoint, 
                        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],
                        hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]))
                    fingersOpen.append(openOrNot(
                        middlePoint,
                        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]))
                    fingersOpen.append(openOrNot(
                        middlePoint, 
                        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
                        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]))
                    fingersOpen.append(openOrNot(
                        middlePoint, 
                        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
                        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]))
                    fingersOpen.append(openOrNot(
                        middlePoint, 
                        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP],
                        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]))

                    secVal(arrayConv(fingersOpen))

                    mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
           
            # Si no se detecta ninguna mano, se indica el ultimo gesto reconocido como vacio
            else: 
                lastGesture = ''
            cv2.imshow('RGM', image)
            if cv2.waitKey(5) & 0xFF == 13:       # Si presionamos Enter
                keepOpen = False
                break
        cap.release()
        cv2.destroyAllWindows()

def predict(imagen,model):
  result = np.argmax(model.predict(imagen) > 0.5).astype("int32")
  #print(result)
  if result == 0:
    return "CincoDedos"
  elif result == 1:
    return "Punio"
  else: return ""

def ampliarImagen(imagen,width,height):
    return cv2.resize(imagen, (width,height), interpolation = cv2.INTER_AREA) 

def recorteImagen(imagen,results,width,height):
    puntos = {'x':[],'y':[]}
    for hand_landmarks in results.multi_hand_landmarks:
        for cont in range(21):
            puntos["x"].append(hand_landmarks.landmark[cont].x)
            puntos["y"].append(hand_landmarks.landmark[cont].y)

    xL = int(width*(min(puntos['x'])))-50
    xR = int(width*(max(puntos['x'])))+50
    yB = int(height*(max(puntos['y'])))+50
    yT = int(height*(min(puntos['y'])))-50
    if xL < 0: 
        xL = 0
    if xR > width: 
        xR = width
    if yT < 0: 
        yT = 0
    if yB > height: 
        yB = height
    #print(xL,xR,yT,yB)
    imageCrop = imagen[yT:yB,xL:xR]
    dim = (50, 50)                        
    # resize image
    try:
        resized = cv2.resize(imageCrop, dim, interpolation = cv2.INTER_AREA)  
    except Exception as e:
        print(str(e))
    
    return resized

def init2(cScene: Scene):
    
    global x
    global y
    global lastGesture
    global keepOpen
    global currentScene

    currentScene = cScene
    timer = threading.Thread(target=clock)
    timer.start()

    # Carga el modelo
    model = keras.models.load_model("modelo.h5")
    print('Modelo cargado')

    cap = cv2.VideoCapture(0)

    # Aqui obtenemos el tamano de X y Y
    x = int (cap.get(3))
    y = int (cap.get(4))
    #print('x: {}, y {}'.format(x,y))

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        max_num_hands=1,
        min_tracking_confidence=0.5
        ) as hands:

        while True:
            ret, frame = cap.read()
            if ret == False:
                break
            height, width, _ = frame.shape
            frame = cv2.flip(frame, 1)            
            actualGesture = ""
            results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imagen = frame[0:50,0:50]
            if results.multi_hand_landmarks is not None:
                imagen = recorteImagen(frame,results,width,height)
                numpydata = asfarray(imagen,dtype='float32')
                x = np.expand_dims(numpydata, axis=0)
                actualGesture = predict(x,model)
                secVal3(actualGesture)
                #print(result)
            else:
                lastGesture = ""
                actualGesture = ""
                frame = frame[0:600,0:600]
                imagen = cv2.resize(frame, (200,200), interpolation = cv2.INTER_AREA) 
            imagen = ampliarImagen(imagen,200,200)
            cv2.putText(imagen,actualGesture,(20,20),cv2.FONT_HERSHEY_DUPLEX,.7,(51,184,255),2)   
            anchoPantalla = GetSystemMetrics(0)
            altoPantalla = GetSystemMetrics(1)
            cv2.imshow("Mano",imagen)  
            cv2.moveWindow("Mano", anchoPantalla-200,altoPantalla-300)
            #cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == 13:
                keepOpen = False
                break
    cap.release()
    cv2.destroyAllWindows

if __name__ == '__main__':
    init2(currentScene)