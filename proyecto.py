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
y = 480
x = 640
timeInSecs = 0
gestureSec = 0
lastGesture = ''

def arrayConv(array) -> str:
    resultStr = ''
    for i in range(5):
        if(array[i]):
            resultStr = resultStr + '1'
        else:
            resultStr = resultStr + '0'
    # print (resultStr)
    return resultStr

def secVal(actualGesture):
    global lastGesture
    global gestureSec
    if lastGesture != actualGesture:
        lastGesture = actualGesture
        gestureSec = timeInSecs
    else:
        if timeInSecs == (gestureSec + 3):
            invokeAction(actualGesture)

def invokeAction(fingers):
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
    
    elif fingers == '11111':
        print ('Gesto 5')
        keyboard.tap(Key.space)

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
        keyboard.tap(Key.esc)

def openOrNot(WRIST, FT, FB):
    global y
    global x
    wristVector = np.array([WRIST[0], WRIST[1]])
    fingerTipVector = np.array([x*FT.x, y*FT.y])
    fingerBaseVector = np.array([x*FB.x, y*FB.y])
    diffFT = np.linalg.norm(wristVector-fingerTipVector)
    diffFB = np.linalg.norm(wristVector-fingerBaseVector)
    # print ('Distance: {}\n'.format(diffFT - diffFB))

    if diffFT-diffFB>0:
        return True
    else:
        return False    
    
def clock():
    global timeInSecs
    global lastGesture
    while True:
        print('Segundo {}, gesto {}'.format(timeInSecs, lastGesture))
        timeInSecs = timeInSecs +1
        time.sleep(1)

def main():

    global x
    global y
    global lastGesture

    timer = threading.Thread(target=clock)
    timer.start()

    # For webcam input:
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
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
            # We need a time counter here to make the program wait for the invokes
            # time.sleep(1)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
        
                    # Here we're creating a new point that indicates the center of the palm
                    wristP = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                    midFB = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                    newCx = int((x*wristP.x + x*midFB.x)/2)
                    newCy = int((y*wristP.y + y*midFB.y)/2)
                    # cv2.circle(image, (newCx,newCy), 3, (100,33,200),2)  
                    middlePoint = [newCx,newCy]

                    fingersOpen = []
                    fingersOpen.append(openOrNot(
                        middlePoint, 
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
           
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()

if __name__ == '__main__':
    main()
