_RAW_TEXT_ = []             # Texto crudo
_SCENE_NAME_ = []               # Estados
_SCENE_DATE_ = []             # Abecedario
_GEST_DICT_ = []            # Estado inicial
_END_STATE_ = []            # Esdatos finales          
_DELTA_ = []                # Transiciones  [origen, trans, final]
_EPSILON_ = 'E'             # Representacion del caracter EPSILON
_VALID_PATHS_ = []          # Caminos validos del automata
_NEW_Q_ = []
_NEW_Q_MERGED_ = []
_NEW_DELTA_ = []
_NEW_END_STATE_ = []
FILEPATH = ''               # Ruta de escenario

def sortGestures(lenght, RAW_DATA):          # Acomoda y normaliza las asociaciones en un arreglo
    i = 2       # Porque en la posicion 2 comienzan las asociaciones
    SORT_DATA = []
    while i < lenght:
        SORT_DATA.insert(len(SORT_DATA),RAW_DATA[i].split(','))
        i += 1
    return SORT_DATA

def agrupaQ(PATHS):                         # Hace el merge de los caminos posibles
    newList = []

    for path in PATHS:
        for state in path:
            try:
                newList.index(state)
            except:
                newList.append(state)
    
    return newList

def recorreSimbolo(newQ, ch):               # Buscamos transiciones con cada letra del alfabeto
    global _DELTA_                          # newQ es una lista, ch es el caracter del alfabeto
    global _NEW_Q_
    new_list_Q = []

    for state in newQ:
        for trans in _DELTA_:
            if str(trans[0]) == str(state) and  str(trans[1]) == ch:
                new_list_Q.append(trans[2])
    if len(new_list_Q) > 0:
        _NEW_Q_.append(new_list_Q)

def recorreEpsilon(edoIni, strMerged):      # Recorre las transiciones posibles por medio de E
    global _DELTA_                          # y las guarda como caminos, para depues poder juntarlas 
    global _VALID_PATHS_                    # en una nueva Q
    global _EPSILON_
    at_least_one = False

    for trans in _DELTA_:
        if trans[0] == edoIni and trans[1] == _EPSILON_:
            at_least_one = True
            recorreEpsilon(trans[2], strMerged+str(trans[0]+','))

    if not at_least_one:
        _VALID_PATHS_.append((str(strMerged)+str(edoIni)).split(','))

def setFILEPATH(path):
    global FILEPATH
    FILEPATH = path

def main():
    # Definimos las listas globales
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
    _GEST_DICT_ = _RAW_TEXT_[2].split(',')          # Guardamos los estados finales

    _DELTA_ = sortGestures(len(_RAW_TEXT_), _RAW_TEXT_)

    # Reordenar las transiciones

    recorreEpsilon(_SCENE_NAME_[0], '')
    _NEW_Q_.append(agrupaQ(_VALID_PATHS_))
    _VALID_PATHS_ = []

    for q in _NEW_Q_:
        for char in _SCENE_DATE_:
            recorreSimbolo(q, char)

    _NEW_Q_[0] = [_SCENE_NAME_[0]]
    
    for q in _NEW_Q_:                                   # Agrupamos las nuevas Q y las metemos
        print(q)                                        # dentro de _NEW_Q_MERGED
        for x in q:
            recorreEpsilon(x,'')
        _NEW_Q_MERGED_.append(agrupaQ(_VALID_PATHS_))
        _VALID_PATHS_ = []

    for Qlist in _NEW_Q_MERGED_:
        print(Qlist)
        list = []
        for state in Qlist:
            for char in _SCENE_DATE_:
                for TRANS in _DELTA_:
                    if str(state) == TRANS[0] and str(char) == TRANS[1]:
                        list.append('Q'+str(_NEW_Q_MERGED_.index(Qlist)))
                        list.append(TRANS[1])
                        for originalQ in _NEW_Q_:
                                for state2 in originalQ:
                                    if str(state2) == str(TRANS[2]):
                                        list.append('Q'+str(_NEW_Q_.index(originalQ)))
        _NEW_DELTA_.append(list)

    for q in _NEW_Q_MERGED_:
        for endState in _END_STATE_:
            try:
                q.index(endState)
                _NEW_END_STATE_.append('Q'+str(_NEW_Q_MERGED_.index(q)))
            except:
                pass


    print(_NEW_DELTA_)
    print(_NEW_END_STATE_)



if __name__ == '__main__':
    main()