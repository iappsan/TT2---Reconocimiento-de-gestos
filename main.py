import tkinter as tk
from tkinter import filedialog

# Globales
defBG = "#303030"
defFontColor = "#E7E7E7"

# Crear la ventana
ventana = tk.Tk()

# Crear menu superior
menuBar = tk.Menu(ventana)
archivoMenu = tk.Menu(menuBar, tearoff=0)
ayudaMenu = tk.Menu(menuBar, tearoff=0)

archivoMenu.add_command(label="Nuevo")
archivoMenu.add_command(label="Abrir")
archivoMenu.add_separator()
archivoMenu.add_command(label="Salir", command=ventana.quit)

ayudaMenu.add_command(label="Ayuda")

menuBar.add_cascade(label="Archivo", menu=archivoMenu)
menuBar.add_cascade(label="Ayuda", menu=ayudaMenu)

# Crear funciones
def newWindow():
    # ventana.withdraw()
    top = tk.Toplevel()
    top.geometry("400x200")
    top.title("ventana nueva")
    button = tk.Button(top, text="OK", command=top.destroy).pack()

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

# Configurar la ventana principal
ventana.title("RGM OPMA") # Reconocimiento de gestos manuales para la organización y presentación de material audiovisual
ventana.geometry("500x300")
ventana.resizable(False,False)
ventana.config(bg=defBG, menu=menuBar)

# Crear un contenido principal
label1 = tk.Label(ventana, text="Bienvenido!", bg=defBG, fg=defFontColor).pack(pady=15)
label2 = tk.Label(ventana, text="Abre o crea un nuevo escenario para continuar:", bg=defBG, fg=defFontColor).pack()

frame1 = tk.Frame(ventana, bd=0).pack(pady=30)
# button1 = tk.Button(ventana, text="Otra ventana", command=newWindow).pack()
button2 = tk.Button(frame1, text="Abrir", command=openFile).pack()
button3 = tk.Button(frame1, text="Crear", command=openFile).pack(pady=10)

# Iniciar el bucle principal de la ventana
ventana.mainloop()