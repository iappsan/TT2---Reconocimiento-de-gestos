from tkinter import *
from tkinter import filedialog
from datetime import date
import os
import proyecto as recognize

# Importamos la clase del escenario
from escenario import Scene

# Globales
defBG = "#303030"
defFontColor = "#E7E7E7"
currentScene = Scene()
tempDirectory = 'tempScenes/'


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
    rowNum = 1

    print ('Escenario en uso:\n'+currentScene._SCENE_NAME_)

    def onClosing():    # Cuando el usuario cierra la ventana, resurge la ventana principal
        root.iconify()
        root.deiconify()
        currentScene.emptypls()
        top.destroy()

    def initRecognize():    # Resetea parametros para empezar o continuar el reconocimiento
        recognize.keepOpen = True
        recognize.init()

    root.withdraw()
    top = Toplevel()
    top.geometry("400x600")
    top.geometry("+400+300")
    top.config(bg=defBG)
    top.title("Configura tu escenario")
    top.protocol('WM_DELETE_WINDOW', onClosing)

    def createGest():
        print (len(_temp_list))
        if len(_temp_list) < 9:

            unusedGest = 10             # Buscamos un gesto qeu no haya sido asignado
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
            print (rowNum)
            setDropdown(unusedGest, rowNum)

    # Boton para el inicio del reconocimiento
    b = Button(top, text="Iniciar reconocimiento", command=initRecognize)
    b.grid(row=0, column=0, pady=10, padx=5)
    b2 = Button(top, text="Nuevo gesto", command=createGest)
    b2.grid(row=0, column=1, pady=10, padx=5)

    def updateGest(gestNum, opt, link):
        for gest in _temp_list:
            if gest[0] == gestNum:
                gest[1] = opt
                gest[2] = link

        currentScene.updateSceneGestures(2, [gestNum, opt, link])   # Mandamos la actualizacion al objeto

    def deleteGest(gestNum):
        i = 0
        for gest in _temp_list:
            if gest[0] == gestNum:
                _temp_list.pop(i)
            else:
                i+=1

        currentScene.updateSceneGestures(3, [gestNum,'',''])

    def setDropdown(gestureAssigned, rowNum):
        gestureSelected = StringVar()
        gestureSelected.set(gestureAssigned)

        optGesturesMenu = OptionMenu(top, gestureSelected, *recognize.actions)
        optGesturesMenu.grid(row=rowNum, column=0, padx=10)

    for gest in currentScene._GEST_DICT_:   # Rellena la nueva lista temporal con los gestos para poder tenerlos en
        _temp_list.append(gest)             # tiempo real
        setDropdown(gest[0], rowNum)
        rowNum += 1


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
        newFile.write(str(date.today()))
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

archivoMenu.add_command(label="Nuevo")
archivoMenu.add_command(label="Abrir")
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