from datetime import date
from pynput.keyboard import Key, Controller
import os


class tempVars:
    temp_entry = ''
    def __init__(self):
        print ('Objeto temporal')   

class Scene:
    
    _FILE_ = ''
    _RAW_TEXT_ = []             # Texto crudo
    _SCENE_NAME_ = ''           # Nombre de escenario
    _SCENE_DATE_ = ''           # Fecha de creacion
    _GEST_DICT_ = []            # Diccionario de gestos con enlaces
                                # El diccionario tiene la siguiente estructura:
                                # [Numerodegesto, 'Accion que hace', 'link si es necesario']

    gestures = ['Gesto 0','Gesto 1','Gesto 2','Gesto 3','Gesto 4','Gesto 5','Gesto 6','Gesto 7','Gesto 8']

    actions = [
        "Abrir archivo",        # 1
        "Abrir enlace",         # 1
        "Siguiente",            # 2
        "Anterior",             # 2
        "Play / Pausa",         # 2
        "Maximizar ventana",    # 2
        "Minimizar ventana",    # 2
        "Cerrar ventana",       # 2
        "Aplicacion siguiente", # 2
        "Aplicacion anterior",  # 2
    ]

    command = [
        '',
        'start ',
    ]

    FILEPATH = ''               # Ruta de escenario

    def __init__(self):
        print ('Escenario seteado')
        for x in range(9):
            self._GEST_DICT_.append([x, '', ''])    

    def loadScene(self, path):
        self.FILEPATH = path
        print("Leyendo escenario ...")

        self._FILE_ = open(path, 'r')
        CONTENIDO = self._FILE_.readlines()

        for line in CONTENIDO:
            self._RAW_TEXT_.append(line.replace('\n',''))
        self._FILE_.close()

        self._SCENE_NAME_ = self._RAW_TEXT_[0]         # Cargamos el titulo
        self._SCENE_DATE_ = self._RAW_TEXT_[1]         # Cargamos la fecha
    
        self._GEST_DICT_ = self.sortGestures(len(self._RAW_TEXT_), self._RAW_TEXT_)

        print ('... Escenario cargado')

    def sortGestures(self, leng, RAW_DATA):      # Acomoda y normaliza las asociaciones en un arreglo
        i = 2                                   # Porque en la posicion 2 comienzan las asociaciones
        SORT_DATA = []
        while i < leng:
            SORT_DATA.insert(len(SORT_DATA),RAW_DATA[i].split(','))
            i += 1
        return SORT_DATA

    def updateSceneGestures(self, opType, _DATA_):      # Se utiliza cada que movemos algo en la configuracion del escenario
                                                # Args: 1:add, mod, del.  2:  
        if opType == 1:
            print ('Add')
            self._GEST_DICT_.insert(len(self._GEST_DICT_),_DATA_)      # Agregamos al final del diccionario el nuevo gesto

        elif opType == 2:
            print ('Mod')

            # print(self._GEST_DICT_)
            self._GEST_DICT_[_DATA_[0]] =_DATA_     # Igualamos el nuevo gesto al que ya estaba definido

            print(self._GEST_DICT_[_DATA_[0]])
            # gestFound = False

            # for gest in self._GEST_DICT_:
            #     if not gestFound:
            #         if gest[0] == _DATA_[0]:        # Si se encuentra el gesto que se busca actualizar
            #             gest = _DATA_               # se actualiza el gesto, la accion y su link
            #             gestFound = True

        elif opType == 3:
            print ('Del')
            gestFound = False
            i = 0

            for gest in self._GEST_DICT_:
                if not gestFound:
                    if gest[0] == _DATA_[0]:        # Si se encuentra el gesto se elimina segun el
                        self._GEST_DICT_.pop(i)     # indice en el que se encuentre
                        gestFound = True
                    else:
                        i+=1

    def separateLists(self,DATA):
        newData = []

        for line in DATA:
            newLine = str(line[0])+','+str(line[1])+','+str(line[2]+'\n')
            newData.append(newLine)
        
        return newData

    def saveScene(self):
        print("Creando archivo para escenario ...")

        newFile = open('tempScenes/'+str(date.today())+self._SCENE_NAME_.replace(' ','')+'.txt','w')
        newFile.write(self._SCENE_NAME_+'\n')
        newFile.write(self._SCENE_DATE_+'\n')
        newFile.writelines(self.separateLists(self._GEST_DICT_))
        newFile.close()

        print('Listo')

    def setFILEPATH(self, path):
        self.FILEPATH = path

    def setSceneName(self, newName):
        self._SCENE_NAME_ = newName

    def invokeAction(self, fingers):      # Identificamos que posicion de gesto es el que identificamos

        if fingers == '00000':
            return 1
        elif fingers == '01000':
            return 2
        elif fingers == '01100':
            return 3
        elif fingers == '00111':
            return 4
        elif fingers == '01111':
            return 5
        elif fingers == '10000':
            return 6
        elif fingers == '11000':
            return 7
        elif fingers == '10001':
            return 8
        elif fingers == '01110':
            return 9
        elif fingers == '11111':        # Con este gesto se detiene el reconocimiento
            print ('GESTO DE SALIDA')
            return 0
    
    def execAct(self, fingerStr):         # Ejecuta las acciones segun su tipo

        keyboard = Controller()

        n = self.invokeAction(fingerStr) - 1
        if n == 0 or n == 1:
            os.system(self.command[n] + self._GEST_DICT_[2])
        elif n == 2:
            keyboard.tap(Key.right)
        elif n == 3:
            keyboard.tap(Key.left)
        elif n == 4:
            keyboard.tap(Key.space)
        elif n == 5:
            keyboard.press(Key.cmd)
            keyboard.tap(Key.up)
            keyboard.release(Key.cmd)
        elif n == 6:
            keyboard.press(Key.cmd)
            keyboard.tap(Key.down)
            keyboard.release(Key.cmd)
        elif n == 7:
            keyboard.press(Key.alt)
            keyboard.tap(Key.tab)
            keyboard.release(Key.alt)
        elif n == 8:
            keyboard.press(Key.alt)
            keyboard.press(Key.shift)
            keyboard.tap(Key.tab)
            keyboard.release(Key.shift)
            keyboard.release(Key.cmd)

    def emptypls(self):
        print ('Vaciando')
        self._FILE_ = ''
        self._RAW_TEXT_ = []             # Texto crudo
        self._SCENE_NAME_ = ''           # Nombre de escenario
        self._SCENE_DATE_ = ''           # Fecha de creacion
        self._GEST_DICT_ = []            # Diccionario de gestos con enlaces
        self.FILEPATH = ''               # Ruta de escenario