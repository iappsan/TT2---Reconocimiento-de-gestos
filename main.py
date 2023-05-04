from tkinter import *
from tkinter import filedialog
from datetime import date

# Globales
defBG = "#303030"
defFontColor = "#E7E7E7"
nombreEscenario = ""
rutaEscenario = ""

# Crear la root
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

# Crear funciones
def newWindow():
    # root.withdraw()
    top2 = Toplevel()
    top2.geometry("400x200")
    top2.title("root nueva")
    button = Button(top2, text="OK", command=top2.destroy).pack()

def windowHelp():
    top = Toplevel()
    top.geometry("400x200")
    top.config(bg=defBG)
    top.title("Ayuda")
    label1 = Label(top, text="Aqui debe aparecer texto o imagenes con ayuda", bg=defBG, fg=defFontColor).pack(pady=15)
    button = Button(top, text="Cerrar", command=top.destroy).place(relx=0.4, rely=0.5)

def windowCreateScene():
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

    nombreEscenario = StringVar()
    e1 = Entry(top, textvariable=nombreEscenario).grid(row=0, column=1)
    e2 = Label(top, text=date.today(), bg=defBG, fg=defFontColor).grid(row=1, column=1)
    button = Button(top, text="Crear escenario", command=top.destroy).place(relx=0.4, rely=0.5)

def openFile():
    try:
        path = filedialog.askopenfilename(
            title="Abrir escenario",
            filetypes=(
                ("Archivos de texto", "*.txt"),
                ("Archivos RGM", "*.rgm"),
            ))
        file = open(path, 'r')
        print (file.read())
    except:
        print("No abriste nada")

# Configurar la root principal
root.title("RGM OPMA") # Reconocimiento de gestos manuales para la organización y presentación de material audiovisual
root.geometry("500x300")
root.resizable(False,False)
root.config(bg=defBG, menu=menuBar)

# Crear un contenido principal
label1 = Label(root, text="Bienvenido!", bg=defBG, fg=defFontColor).pack(pady=15)
label2 = Label(root, text="Abre o crea un nuevo escenario para continuar:", bg=defBG, fg=defFontColor).pack()

# button1 = Button(root, text="Otra root", command=newWindow).pack()
b2 = Button(root, text="Abrir", command=openFile).pack(pady=(50,10))
b3 = Button(root, text="Crear", command=windowCreateScene).pack()
b4 = Button(root, text="?", bg=defBG, fg=defFontColor, command=windowHelp).place(x=450, y=10)

root.mainloop()