import keras
import cv2
import numpy as np

# Load the model
model = keras.models.load_model("modeloGestos.h5")
print('Model loaded')


# Create function to match label to letter
def getLetter(result):
    classLabels = {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'D',
        4: 'E',
        5: 'F',
        6: 'G',
        7: 'H',
        8: 'I',
        9: 'K',
        10: 'L',
        11: 'M',
        12: 'N',
        13: 'O',
        14: 'P',
        15: 'Q',
        16: 'R',
        17: 'S',
        18: 'T',
        19: 'U',
        20: 'V',
        21: 'W',
        22: 'X',
        23: 'Y'
    }
    try:
        res = int(result)
        return classLabels[res]
    except:
        print(result)
        return "Error"
    
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # frame = cv2.flip(frame,1)

    # Define region of interest
    roi = frame[100:400, 320:620]
    cv2.imshow('roi', roi)
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    roi = cv2.resize(roi, (28,28), interpolation = cv2.INTER_AREA)

    cv2.imshow('roi scaled and gray', roi)
    copy = frame.copy()
    cv2.rectangle(copy, (320,100), (620,400), (255,0,0), 5)

    roi = roi.reshape(1,28,28,1)

    # result = str(model.predict_classes(roi, verbose=0)[0])
    predictions = np.argmax(model.predict(roi, verbose=0), axis=-1)
    print (predictions)
    cv2.putText(copy, 
                getLetter(predictions), 
                (300,100), 
                cv2.FONT_HERSHEY_COMPLEX,
                2,
                (0,255,0),
                2
                )
    cv2.imshow('frame', copy)

    if cv2.waitKey(1) == 13: # Enter
        break

cap.release()
cv2.destroyAllWindows