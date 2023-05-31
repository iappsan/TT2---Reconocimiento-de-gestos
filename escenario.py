class Scene:
    
    _FILE_ = ''
    _RAW_TEXT_ = []             # Texto crudo
    _SCENE_NAME_ = ''           # Nombre de escenario
    _SCENE_DATE_ = ''           # Fecha de creacion
    _GEST_DICT_ = []            # Diccionario de gestos con enlaces

    FILEPATH = ''               # Ruta de escenario

    def sortGestures(self, len, RAW_DATA):    # Acomoda y normaliza las asociaciones en un arreglo
        i = 2                           # Porque en la posicion 2 comienzan las asociaciones
        SORT_DATA = []
        while i < len:
            SORT_DATA.insert(len(SORT_DATA),RAW_DATA[i].split(','))
            i += 1
        return SORT_DATA

    def _init_(self, file):

        print("Leyendo escenario ...")

        self._FILE_ = file
        CONTENIDO = file.readlines()
        for line in CONTENIDO:
            self._RAW_TEXT_.append(line.replace('\n',''))
        file.close()

        self._SCENE_NAME_ = self._RAW_TEXT_[0]         # Cargamos el titulo
        self._SCENE_DATE_ = self._RAW_TEXT_[1]         # Cargamos la fecha
    
        self._GEST_DICT_ = self.sortGestures(len(self._RAW_TEXT_), self._RAW_TEXT_)

    

    def updateSceneGestures(self, opType, _DATA_):      # Se utiliza cada que movemos algo en la configuracion del escenario
                                                # Args: 1:add, mod, del.  2:  
        if opType == 1:
            print ('Add')
            self._GEST_DICT_.insert(_DATA_)      # Agregamos al final del diccionario el nuevo gesto

        elif opType == 2:
            print ('Mod')
            gestFound = False

            for gest in self._GEST_DICT_:
                if not gestFound:
                    if gest[0] == _DATA_[0]:        # Si se encuentra el gesto que se busca actualizar
                        gest = _DATA_               # se actualiza el gesto, la accion y su link
                        gestFound = True

        elif opType == 3:
            print ('Del')
            gestFound = False
            i = 0

            for gest in self._GEST_DICT_:
                if not gestFound:
                    if gest[0] == _DATA_[0]:        # Si se encuentra el gesto se elimina segun el
                        self._GEST_DICT_.pop(i)     # indice en el que se encuentre
                    else:
                        i+=1

    def separateLists(self,DATA):
        newData = []

        for line in DATA:
            newLine = line[0]+','+line[1]+','+line[2]
            newData.append(newLine)
        
        return newData

    def saveScene(self):
        print("Creando archivo para escenario ...")

        newFile = open('.\\Escenarios\\'+self._SCENE_NAME_.replace(' ','')+'.txt','w')
        newFile.write(self._SCENE_NAME_)
        newFile.write(self._SCENE_DATE_)
        newFile.writelines(self.separateLists(self._GEST_DICT_))
        newFile.close()

        print('Listo')

    def setFILEPATH(self, path):
        self.FILEPATH = path

    def setSceneName(self, newName):
        self._SCENE_NAME_ = newName
