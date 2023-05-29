class Scene:
    
    _RAW_TEXT_ = []             # Texto crudo
    _SCENE_NAME_ = ''           # Nombre de escenario
    _SCENE_DATE_ = ''           # Fecha de creacion
    _GEST_DICT_ = []            # Diccionario de gestos con enlaces

    FILEPATH = ''               # Ruta de escenario

    def sortGestures(lenght, RAW_DATA):          # Acomoda y normaliza las asociaciones en un arreglo
        i = 2       # Porque en la posicion 2 comienzan las asociaciones
        SORT_DATA = []
        while i < lenght:
            SORT_DATA.insert(len(SORT_DATA),RAW_DATA[i].split(','))
            i += 1
        return SORT_DATA

    def loadScene(args):
        global _RAW_TEXT_
        global _SCENE_NAME_
        global _SCENE_DATE_
        global _GEST_DICT_

        print("Leyendo escenario ...")

        file = open (FILEPATH, 'r')
        CONTENIDO = file.readlines()
        for line in CONTENIDO:
            _RAW_TEXT_.append(line.replace('\n',''))
        file.close()

        _SCENE_NAME_ = _RAW_TEXT_[0]         # Cargamos el titulo
        _SCENE_DATE_ = _RAW_TEXT_[1]         # Cargamos la fecha
    
        _GEST_DICT_ = sortGestures(len(_RAW_TEXT_), _RAW_TEXT_)

    def updateScene(opType, _DATA_):        # Se utiliza cada que movemos algo en la configuracion del escenario
        global _GEST_DICT_                  # Args: 1:add, mod, del.  2:  

        if opType == 1:
            print ('Add')
            _GEST_DICT_.insert(_DATA_)      # Agregamos al final del diccionario el nuevo gesto

        elif opType == 2:
            print ('Mod')
            gestFound = False

            for gest in _GEST_DICT_:
                if not gestFound:
                    if gest[0] == _DATA_[0]:        # Si se encuentra el gesto que se busca actualizar
                        gest = _DATA_               # se actualiza el gesto, la accion y su link
                        gestFound = True

        elif opType == 3:
            print ('Del')
            gestFound = False
            i = 0

            for gest in _GEST_DICT_:
                if not gestFound:
                    if gest[0] == _DATA_[0]:        # Si se encuentra el gesto se elimina segun el
                        _GEST_DICT_.pop(i)          # indice en el que se encuentre
                    else:
                        i+=1

    def saveScene():
        global _RAW_TEXT_
        global _SCENE_NAME_
        global _SCENE_DATE_
        global _GEST_DICT_

        print("Creando archivo para escenario ...")

        newFile = open('.\\Escenarios\\'+_SCENE_NAME_.replace(' ','')+'.txt','w')
        newFile.write(_SCENE_NAME_)
        newFile.write(_SCENE_DATE_)
        newFile.writelines(_GEST_DICT_)
        newFile.close()

        print('Listo')


    def setFILEPATH(path):
        global FILEPATH
        FILEPATH = path