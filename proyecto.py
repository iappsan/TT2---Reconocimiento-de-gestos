import cv2
import os
import numpy as np
import mediapipe as mp
import threading
import time
from pynput.keyboard import Key, Controller

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
y = 0
x = 0
timeInSecs = 0
gestureSec = 0
lastGesture = ''
keepOpen = True

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

def secVal(actualGesture):      # Validamos que el gesto dure 3 segundos por medio de un contador
    global lastGesture
    global gestureSec
    if lastGesture != actualGesture:
        lastGesture = actualGesture
        gestureSec = timeInSecs
    else:
        if timeInSecs == (gestureSec + 3):
            invokeAction(actualGesture)
            gestureSec = 0      # Reiniciamos el contador para que solo se ejecute una vez la accion

def invokeAction(fingers):      # Invocamos las acciones que cada gesto debe de hacer
    keyboard = Controller()

    if fingers == '01000':
        print ('Gesto 1')
        keyboard.tap(Key.f5)
    elif fingers == '01100':
        print ('Gesto 2')
        keyboard.tap(Key.right)
    elif fingers == '00111':
        print ('Gesto 3')
        os.system('explorer "https://netflix.com"')

    elif fingers == '01111':
        print ('Gesto 4')

    elif fingers == '00000':
        print ('Gesto 6')
    elif fingers == '10000':
        print ('Gesto 7')
        keyboard.tap(Key.left)
    elif fingers == '11000':
        print ('Gesto 8')
    elif fingers == '10001':
        print ('Gesto 9')
    elif fingers == '01110':
        print ('Gesto 10')

    elif fingers == '11111':        # Con este gesto se detiene el reconocimiento
        print ('Gesto 5')
        global keepOpen
        keepOpen = False
        

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

def init():

    global x
    global y
    global lastGesture
    global keepOpen

    timer = threading.Thread(target=clock)
    timer.start()

    # For webcam input:
    cap = cv2.VideoCapture(0)

    # Here we get the x,y size
    x = int (cap.get(3))
    y = int (cap.get(4))
    print('x: {}, y {}'.format(x,y))

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened() and keepOpen:
            success, image = cap.read()
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
        
                    # Here we're creating a new point that indicates the center of the palm
                    wristP = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    midFB = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                    newCx = int((x*wristP.x + x*midFB.x)/2)
                    newCy = int((y*wristP.y + y*midFB.y)/2)
                    cv2.circle(image, (newCx,newCy), 3, (100,33,200),2)  
                    middlePoint = [newCx,newCy]
                    # New point for the thumb
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
           
            # Si no se detecta ninguna mano, seteamos el ultimo gesto reconocido a vacio
            else: 
                lastGesture = ''
            # Voltea la image horizontalmente
            cv2.imshow('RGM', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == ord('q'):       # Si presionamos la tecla Q, salimos
                keepOpen = False
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    init()