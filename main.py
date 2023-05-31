from tkinter import *
from tkinter import filedialog
from datetime import date
import os

# Importamos la clase del escenario
from escenario import Scene

# Globales
defBG = "#303030"
defFontColor = "#E7E7E7"
currentScene = ''
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
    root.withdraw()
    top = Toplevel()
    top.geometry("400x200")
    top.config(bg=defBG)
    top.title("Configura tu escenario")

    b = Button(top, text="Iniciar reconocimiento", command=top.destroy)
    b.place(relx=0.37, rely=0.2)

def windowCreateScene():    # Ventana de creacion de escenario
    top = Toplevel(root)
    top.geometry("400x200")
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

        print('Listo')

        # Se crea el objeto Scene para poder trabajar con el en la siguiente ventana
        currentScene = Scene(tempDirectory+str(date.today())+newName.replace(' ','')+'.txt')

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
    currentScene = 0

    try:
        path = filedialog.askopenfilename(
            title="Abrir escenario",
            filetypes=(
                ("Archivos de texto", "*.txt"),
                ("Archivos RGM", "*.rgm"),
            ))
        
        # print ('Ya se va a enviar')
        # PASAR "path" HACIA escenario.py PARA INTERACTUAR CON LOS ESCENARIOS
        currentScene = Scene(path)
        # print ('Ya se envio')

        print (currentScene._SCENE_NAME_)
        print (currentScene._SCENE_DATE_)
        print (len(currentScene._GEST_DICT_))
        
        # Inicializar ventana de configuracion

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
root.resizable(False,False)
root.config(bg=defBG, menu=menuBar)

# Crear un contenido principal
label1 = Label(root, text="Bienvenido!", bg=defBG, fg=defFontColor).pack(pady=15)
label2 = Label(root, text="Abre o crea un nuevo escenario para continuar:", bg=defBG, fg=defFontColor).pack()

b2 = Button(root, text="Abrir", command=openFile).pack(pady=(50,10))
b3 = Button(root, text="Crear", command=windowCreateScene).pack()
b4 = Button(root, text="config", command=windowConfigScene).pack()
b5 = Button(root, text="?", bg=defBG, fg=defFontColor, command=windowHelp).place(x=450, y=10)

root.mainloop()