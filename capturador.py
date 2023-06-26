import cv2
import keras

def init2(cScene: Scene):
    
    global x
    global y
    global lastGesture
    global keepOpen
    global currentScene

    currentScene = cScene

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
