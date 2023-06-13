from tkinter import *
from tkinter import filedialog
from datetime import date
import os
from PIL import ImageTk, Image
import proyecto as recognize
from tkinter import ttk
import time

# Importamos la clase del escenario
from escenario import Scene

# Globales
defBG = "#303030"
defFontColor = "#E7E7E7"
currentScene = Scene()
tempDirectory = 'tempScenes/'
ipadding = {'ipadx': 10, 'ipady': 10}


# Crear funciones
def newWindow():            # Template para nuevas ventanas
    # root.withdraw()
    top2 = Toplevel()
    top2.geometry("400x200")
    top2.title("root nueva")
    button = Button(top2, text="OK", command=top2.destroy).pack()

def windowHelp():           # Ventana de ayuda
    top = Toplevel()
    top.geometry("400x200")
    top.config(bg=defBG)
    top.title("Ayuda")
    label1 = Label(top, text="Aqui debe aparecer texto o imagenes con ayuda", bg=defBG, fg=defFontColor).pack(pady=15)
    button = Button(top, text="Cerrar", command=top.destroy).place(relx=0.4, rely=0.5)

def windowConfigScene():    # Ventana de configuracion de escenario
    global currentScene
    _temp_list = []

    def onClosing():    # Cuando el usuario cierra la ventana, resurge la ventana principal
        root.iconify()
        root.deiconify()
        currentScene.emptypls()
        top.destroy()

    def initRecognize():    # Resetea parametros para empezar o continuar el reconocimiento
        global currentScene
        recognize.keepOpen = True
        recognize.init(currentScene)

    root.withdraw()
    top = Toplevel()
    top.geometry("900x600")
    top.geometry("+400+300")
    top.config(bg=defBG)
    top.title("Configura tu escenario")
    top.protocol('WM_DELETE_WINDOW', onClosing)

    # Cambiamos la forma de crear links con gestos, entonces la sig funcion createGest() esta en desuso por ahora
    def createGest():
        print (len(_temp_list))
        if len(_temp_list) < 9:

            unusedGest = 10             # Buscamos un gesto que no haya sido asignado
            for i in range(9):
                used = False
                for gest in _temp_list:
                    if gest[0] == i:
                        used = True
                if not used:
                    unusedGest = i
                    break

            _temp_list.append([unusedGest, '',''])      #lo agregamos con acciones vacias
            currentScene.updateSceneGestures(1, _temp_list[len(_temp_list)-1])  # Lo mandamos al objeto
            setDropdown(unusedGest)

    def saveScene():        # Solo guarda el escenario desde la clase
        global currentScene
        currentScene.saveScene()

    def refreshScene():
        global currentScene

        print('\n')
        print('\n')
        print('\n')
        temp_list = []
        temp_list.append(action_list.get())
        temp_list.append(action_list2.get())
        temp_list.append(action_list3.get())
        temp_list.append(action_list4.get())
        temp_list.append(action_list5.get())
        temp_list.append(action_list6.get())
        temp_list.append(action_list7.get())
        temp_list.append(action_list8.get())
        temp_list.append(action_list9.get())
        # print(temp_list)

        for x in range(9):
            link = ''
            if temp_list[x] == currentScene.actions[0] or temp_list[x] == currentScene.actions[1]:
                # print (currentScene._GEST_DICT_[x])
                link = currentScene._GEST_DICT_[x][2]
            currentScene.updateSceneGestures(2,[x, temp_list[x], link])
        
        currentScene.saveScene()


    # Boton para el inicio del reconocimiento
    b = Button(top, text="Iniciar reconocimiento", command=initRecognize)
    b.grid(row=0, column=2, pady=10)
    # Boton para guardar cambios
    b2 = Button(top, text="Guardar cambios", command=saveScene)
    b2.grid(row=0, column=3, pady=10)
    # Boton para actualizar etiquetas
    b3 = Button(top, text="Actualizar", command=refreshScene)
    b3.grid(row=0, column=5, pady=10)

    def splitPaths(pathToSplit: str):
        newStrList = pathToSplit.split('/')
        print( newStrList)
        return newStrList[-1]

    def getPath():
        try:
            path = filedialog.askopenfilename(
                title="Archivo a vincular",
                filetypes=(
                    ("Archivos de texto", "*.txt"),
                    ("PDF", "*.pdf"),
                    ("Power Point","*.pptx"),
                    ("Word","*.docx"),
                    ("Excel","*.xlsx")
                ))
            return path
        except Exception as e:
            print("No abriste nada")
            print(e)

    def getLink(gestNum, opt):
        top2 = Toplevel()
        top2.geometry("400x200")
        top2.title("Ingresa el link")

        def close_window():
            global currentScene
            currentScene.updateSceneGestures(2, [gestNum, opt, E.get()])
            top2.destroy()

        E = Entry(top2)
        E.pack(anchor = CENTER)
        B = Button(top2, text = "Enviar", command = close_window)
        B.pack(anchor = S)

    def updateGest(gestNum, opt, link):
        global currentScene
        if opt == currentScene.actions[0]:
            link = getPath()
            currentScene.updateSceneGestures(2, [gestNum, opt, link])   # Mandamos la actualizacion al objeto
        elif opt == currentScene.actions[1]:
            getLink(gestNum, opt)

    def updateLabels():
        global currentScene
        for x in range(9):
            if currentScene._GEST_DICT_[x][1] == currentScene.actions[0] or currentScene._GEST_DICT_[x][1] == currentScene.actions[1]:
                link = splitPaths(currentScene._GEST_DICT_[x][2])
                linkLabel = Label(top, text=link)
                linkLabel.config(width=5)
                if x > 5:
                    linkLabel.grid(row=x-4, column=5)
                else:
                    linkLabel.grid(row=x+1, column=2)

    def deleteGest(gestNum):
        i = 0
        for gest in _temp_list:
            if gest[0] == gestNum:
                _temp_list.pop(i)
            else:
                i+=1

        currentScene.updateSceneGestures(3, [gestNum,'',''])

    def getLoadedGest(gestNum):
        global currentScene
        if len(currentScene._GEST_DICT_[gestNum][1]) > 0:
            for x in range(9):
                if currentScene._GEST_DICT_[gestNum][1] == currentScene.actions[x]:
                    return x
        return 100

    # COMIENZO DE MENU DE GESTOS
    
    tempStr = ''
    # 0
    rowGe = 1 
    img = PhotoImage(file= "img/gestures/0.png")
    gLabel = Label(top, image=img)
    gLabel.image = img
    gLabel.grid(row=rowGe, column=0, padx=25, pady=5)

    action_list = ttk.Combobox(top, width=18, state='readonly')
    action_list['values'] = currentScene.actions
    tempStr = getLoadedGest(0)
    if tempStr < 99:
        action_list.current(tempStr)
    action_list.bind('<<ComboboxSelected>>', lambda event: updateGest(0, action_list.get(), ''))
    action_list.grid(row=rowGe, column=1)

    # 1
    rowGe = 2 
    img2 = PhotoImage(file= "img/gestures/1.png")
    gLabel2 = Label(top, image=img2)
    gLabel2.image = img2
    gLabel2.grid(row=rowGe, column=0, padx=25, pady=5)

    action_list2 = ttk.Combobox(top, width=18, state='readonly')
    action_list2['values'] = currentScene.actions
    tempStr = getLoadedGest(1)
    if tempStr < 99:
        action_list2.current(tempStr)
    action_list2.bind('<<ComboboxSelected>>', lambda event: updateGest(1, action_list2.get(), ''))
    action_list2.grid(row=rowGe, column=1)

    # 2
    rowGe = 3 
    img3 = PhotoImage(file= "img/gestures/2.png")
    gLabel3 = Label(top, image=img3)
    gLabel3.image = img3
    gLabel3.grid(row=rowGe, column=0, padx=25, pady=5)

    action_list3 = ttk.Combobox(top, width=18, state='readonly')
    action_list3['values'] = currentScene.actions
    tempStr = getLoadedGest(2)
    if tempStr < 99:
        action_list3.current(tempStr)
    action_list3.bind('<<ComboboxSelected>>', lambda event: updateGest(2, action_list3.get(), ''))
    action_list3.grid(row=rowGe, column=1)
    
    # 3
    rowGe = 4 
    img4 = PhotoImage(file= "img/gestures/3.png")
    gLabel4 = Label(top, image=img4)
    gLabel4.image = img4
    gLabel4.grid(row=rowGe, column=0, padx=25, pady=5)

    action_list4 = ttk.Combobox(top, width=18, state='readonly')
    action_list4['values'] = currentScene.actions
    tempStr = getLoadedGest(3)
    if tempStr < 99:
        action_list4.current(tempStr)
    action_list4.bind('<<ComboboxSelected>>', lambda event: updateGest(3, action_list4.get(), ''))
    action_list4.grid(row=rowGe, column=1)

    # 4
    rowGe = 5 
    img5 = PhotoImage(file= "img/gestures/4.png")
    gLabel5 = Label(top, image=img5)
    gLabel5.image = img5
    gLabel5.grid(row=rowGe, column=0, padx=25, pady=5)

    action_list5 = ttk.Combobox(top, width=18, state='readonly')
    action_list5['values'] = currentScene.actions
    tempStr = getLoadedGest(4)
    if tempStr < 99:
        action_list5.current(tempStr)
    action_list5.bind('<<ComboboxSelected>>', lambda event: updateGest(4, action_list5.get(), ''))
    action_list5.grid(row=rowGe, column=1)
    
    # 5
    rowGe = 6 
    img6 = PhotoImage(file= "img/gestures/5.png")
    gLabel6 = Label(top, image=img6)
    gLabel6.image = img6
    gLabel6.grid(row=rowGe-5, column=3, padx=25, pady=5)

    action_list6 = ttk.Combobox(top, width=18, state='readonly')
    action_list6['values'] = currentScene.actions
    tempStr = getLoadedGest(5)
    if tempStr < 99:
        action_list6.current(tempStr)
    action_list6.bind('<<ComboboxSelected>>', lambda event: updateGest(5, action_list6.get(), ''))
    action_list6.grid(row=rowGe-5, column=4)

    # 6
    rowGe = 7 
    img7 = PhotoImage(file= "img/gestures/6.png")
    gLabel7 = Label(top, image=img7)
    gLabel7.image = img7
    gLabel7.grid(row=rowGe-5, column=3, padx=25, pady=5)

    action_list7 = ttk.Combobox(top, width=18, state='readonly')
    action_list7['values'] = currentScene.actions
    tempStr = getLoadedGest(6)
    if tempStr < 99:
        action_list7.current(tempStr)
    action_list7.bind('<<ComboboxSelected>>', lambda event: updateGest(6, action_list7.get(), ''))
    action_list7.grid(row=rowGe-5, column=4)

    # 7
    rowGe = 8 
    img8 = PhotoImage(file= "img/gestures/7.png")
    gLabel8 = Label(top, image=img8)
    gLabel8.image = img8
    gLabel8.grid(row=rowGe-5, column=3, padx=25, pady=5)

    action_list8 = ttk.Combobox(top, width=18, state='readonly')
    action_list8['values'] = currentScene.actions
    tempStr = getLoadedGest(7)
    if tempStr < 99:
        action_list8.current(tempStr)
    action_list8.bind('<<ComboboxSelected>>', lambda event: updateGest(7, action_list8.get(), ''))
    action_list8.grid(row=rowGe-5, column=4)

    # 8
    rowGe = 9 
    img9 = PhotoImage(file= "img/gestures/8.png")
    gLabel9 = Label(top, image=img9)
    gLabel9.image = img9
    gLabel9.grid(row=rowGe-5, column=3, padx=25, pady=5)

    action_list9 = ttk.Combobox(top, width=18, state='readonly')
    action_list9['values'] = currentScene.actions
    tempStr = getLoadedGest(8)
    if tempStr < 99:
        action_list9.current(tempStr)
    action_list9.bind('<<ComboboxSelected>>', lambda event: updateGest(8, action_list9.get(), ''))
    action_list9.grid(row=rowGe-5, column=4)

    updateLabels()

    # FIN DE MENU DE GESTOS

    for gest in currentScene.gestures:   # Rellena la nueva lista temporal con los gestos para poder tenerlos en
        _temp_list.append(gest)          # tiempo real

def windowCreateScene():    # Ventana de creacion de escenario
    top = Toplevel(root)
    top.geometry("400x200")
    top.geometry("+400+400")
    top.config(bg=defBG)
    top.title("Crear un nuevo escenario")
    # frame2 = Frame(top, bd=5, relief="sunken", padx=20, pady=20).pack()
    l1 = Label(top, 
                     text="Nombre del escenario:", 
                     bg=defBG, 
                     fg=defFontColor)
    l1.grid(row=0,column=0)
    l2 = Label(top,
                     text="Fecha de creacion:", 
                     bg=defBG, 
                     fg=defFontColor)
    l2.grid(row=1,column=0)
    
    def sceneCreation():            # Funcion para crear el nuevo escenario
        global currentScene
        global tempDirectory
        newName = e1.get()

        newFile = open(tempDirectory+str(date.today())+newName.replace(' ','')+'.txt','w')
        newFile.write(newName+'\n')
        newFile.write(str(date.today())+'\n')
        for x in range(8):
            newFile.write(str(x)+', '+', \n')
        newFile.write('8, , ')
        newFile.close()

        # Se crea el objeto Scene para poder trabajar con el en la siguiente ventana
        currentScene.loadScene(tempDirectory+str(date.today())+newName.replace(' ','')+'.txt')

        top.destroy()
        windowConfigScene()

    e1 = Entry(top)
    e1.grid(row=0, column=1, pady=30, padx=20)
    e1.focus()
    label2 = Label(top, text=date.today(), bg=defBG, fg=defFontColor)
    label2.grid(row=1, column=1)
    button = Button(top, text="Crear escenario", command=sceneCreation)
    button.place(relx=0.4, rely=0.5)

def openFile():             # Funcion para abrir archivo de escenario

    global currentScene

    try:
        path = filedialog.askopenfilename(
            title="Abrir escenario",
            filetypes=(
                ("Archivos de texto", "*.txt"),
                ("Archivos RGM", "*.rgm"),
            ))
        
        # print ('Ya se va a enviar')
        # PASAR "path" HACIA escenario.py PARA INTERACTUAR CON LOS ESCENARIOS
        currentScene.loadScene(path)
        # print ('Ya se envio')

        # Las siguientes 3 lineas sirven para ver le contenido de un archivo de escenario
        # no son necesarias en la practica:
        # print (currentScene._SCENE_NAME_)
        # print (currentScene._SCENE_DATE_)
        # print (len(currentScene._GEST_DICT_))
        
        # Inicializar ventana de configuracion
        windowConfigScene()

    except Exception as e:
        print("No abriste nada")
        print(e)


try:
    os.mkdir('tempScenes')
    print ('Es la primera vez que se ejecuta el programa')
except Exception as ex:
    print ('No es la primera')

root = Tk()

# Crear menu superior
menuBar = Menu(root)
archivoMenu = Menu(menuBar, tearoff=0)
ayudaMenu = Menu(menuBar, tearoff=0)

archivoMenu.add_command(label="Nuevo", command=windowCreateScene)
archivoMenu.add_command(label="Abrir", command=openFile)
archivoMenu.add_separator()
archivoMenu.add_command(label="Salir", command=root.quit)

ayudaMenu.add_command(label="Ayuda")

menuBar.add_cascade(label="Archivo", menu=archivoMenu)
menuBar.add_cascade(label="Ayuda", menu=ayudaMenu)

# Configurar la root principal
root.title("RGM OPMA") # Reconocimiento de gestos manuales para la organización y presentación de material audiovisual
root.geometry("500x300")
root.geometry("+750+300")
root.resizable(False,False)
root.config(bg=defBG, menu=menuBar)

# Crear un contenido principal
label1 = Label(root, text="Bienvenido!", bg=defBG, fg=defFontColor).pack(pady=15)
label2 = Label(root, text="Abre o crea un nuevo escenario para continuar:", bg=defBG, fg=defFontColor).pack()

b2 = Button(root, text="Abrir", command=openFile).pack(pady=(50,10))
b3 = Button(root, text="Crear", command=windowCreateScene).pack()
# b4 = Button(root, text="config", command=windowConfigScene).pack()
b5 = Button(root, text="?", bg=defBG, fg=defFontColor, command=windowHelp).place(x=450, y=10)

root.mainloop()