from tkinter import *
from tkinter import filedialog
from datetime import date
import threading
from PIL import ImageTk, Image
import proyecto as recognize
from tkinter import ttk
import os


# Importamos la clase del escenario
from escenario import Scene

# Globales
defBG = "#303030"
defFontColor = "#E7E7E7"
currentScene = Scene()
tempDirectory = 'tempScenes/'
ipadding = {'ipadx': 10, 'ipady': 10}

colorFondo = "#60656F"
colorFuente = "#F7F7FF"
tercerColor = "#008CBA"
cuartoColor = "#e7e7e7"
quintoColor = "#4CAF50"
nombreEscenario = ""
rutaEscenario = ""
manual = ["principal.png","crearNuevo.png","abrir.png","configuracion.png","guardarEnlace.png","reconocimiento.png"]
manulActual = 0
textoManual = [
    "Al iniciar el sistema podrás abrir, editar o crear un nuevo escenario con los botones centrales, o abrir la ayuda con el botón ?",
    "Para crear un nuevo escenario solo es necesario el nombre del nuevo escenario, se coloca automáticamente la fecha del día",
    "Para abrir un escenario,selecciona el archivo con el nombre del escenario que requieras",
    "Para editar el escenario, selecciona la acción a realizar con cada gesto que necesites",
    "Si requieres colocar un enlace, se abrirá una ventana para colocarlo",
    "Al presionar 'Iniciar reconocimiento', se abrirá una ventana al inferior derecho de la pantalla para visualizar el gesto identificado"
]


class RoundedButton(Canvas):

    def __init__(self, master=None, text:str="", ancho=240,radius=30, btnforeground=colorFuente, btnbackground=colorFondo, clicked=None, *args, **kwargs):
        super(RoundedButton, self).__init__(master, *args, **kwargs)
        self.config(bg=self.master["bg"])
        self.btnbackground = btnbackground
        self.clicked = clicked
        
        self.radius = radius        
        self['height']=50                   #Tamaño alto
        self['width']=ancho                   #Tamaño ancho
        self['highlightthickness'] = 0      #Quitar margen canvas
        
        self.rect = self.round_rectangle(0, 0, 0, 0, tags="button", radius=radius, fill=btnbackground)
        self.text = self.create_text(0, 0, text=text, tags="button", fill=btnforeground, font=("Century Gothic", 16), justify="center")

        self.tag_bind("button", "<ButtonPress>", self.border)
        self.tag_bind("button", "<ButtonRelease>", self.border)
        self.bind("<Configure>", self.resize)
        
        text_rect = self.bbox(self.text)
        if int(self["width"]) < text_rect[2]-text_rect[0]:
            self["width"] = (text_rect[2]-text_rect[0]) + 10
        
        if int(self["height"]) < text_rect[3]-text_rect[1]:
            self["height"] = (text_rect[3]-text_rect[1]) + 10
          
    def round_rectangle(self, x1, y1, x2, y2, radius=25, update=False, **kwargs): # if update is False a new rounded rectangle's id will be returned else updates existing rounded rect.
        # source: https://stackoverflow.com/a/44100075/15993687
        points = [x1+radius, y1,
                x1+radius, y1,
                x2-radius, y1,
                x2-radius, y1,
                x2, y1,
                x2, y1+radius,
                x2, y1+radius,
                x2, y2-radius,
                x2, y2-radius,
                x2, y2,
                x2-radius, y2,
                x2-radius, y2,
                x1+radius, y2,
                x1+radius, y2,
                x1, y2,
                x1, y2-radius,
                x1, y2-radius,
                x1, y1+radius,
                x1, y1+radius,
                x1, y1]

        if not update:
            return self.create_polygon(points, **kwargs, smooth=True)
        
        else:
            self.coords(self.rect, points)

    def resize(self, event):
        text_bbox = self.bbox(self.text)

        if self.radius > event.width or self.radius > event.height:
            radius = min((event.width, event.height))

        else:
            radius = self.radius

        width, height = event.width, event.height

        if event.width < text_bbox[2]-text_bbox[0]:
            width = text_bbox[2]-text_bbox[0] + 30
        
        if event.height < text_bbox[3]-text_bbox[1]:  
            height = text_bbox[3]-text_bbox[1] + 30
        
        self.round_rectangle(5, 5, width-5, height-5, radius, update=True)

        bbox = self.bbox(self.rect)

        x = ((bbox[2]-bbox[0])/2) - ((text_bbox[2]-text_bbox[0])/2)
        y = ((bbox[3]-bbox[1])/2) - ((text_bbox[3]-text_bbox[1])/2)

        self.moveto(self.text, x, y)

    def border(self, event):
        if event.type == "4":
            self.itemconfig(self.rect, fill=cuartoColor)
            if self.clicked is not None:
                self.clicked()
        else:
            self.itemconfig(self.rect, fill=self.btnbackground)


# Crear funciones
def newWindow():            # Template para nuevas ventanas
    # root.withdraw()
    top2 = Toplevel()
    anchoVentana = 400         #Definir medidas de ventana
    altoVentana = 200
    xVentana = root.winfo_screenwidth() // 2 - anchoVentana // 2  #Definir posición de la ventana
    yVentana = root.winfo_screenheight() // 2 - altoVentana // 2
    posicion = str(anchoVentana) + "x" + str(altoVentana) + \
        "+" + str(xVentana) + "+" + str(yVentana)
    top2.title("root nueva")
    top2.geometry(posicion)
    top2.resizable(False, False)    #La ventana no se puede alargar ni ensanchar

    button = Button(top2, text="OK", command=top2.destroy).pack()

def siguienteImagen(top,lblImage,texto):
    global manulActual
    manulActual = manulActual + 1
    if (manulActual == len(manual) ):
        manulActual = 0
    insertarImagen(top,lblImage,texto)



def anteriorImagen(top,lblImage,texto):
    global manulActual
    manulActual = manulActual - 1
    if (manulActual < -1 ):
        manulActual = len(manual) - 1
    insertarImagen(top,lblImage,texto)



def insertarImagen(top,lblImage,texto):
    img = PhotoImage(file= "img/manual/"+manual[manulActual])
    if manulActual < 2 :
        img = img.subsample(1,1)
    elif manulActual < len(manual) - 1 :
        img = img.subsample(2,2)
    else:
        img = img.subsample(3,3)
    lblImg = Label(top,background=colorFondo,borderwidth=1,image=img,width=900,height=520)
    lblImage.image = img
    lblImg.grid(row=1,column=1)
    texto.set(textoManual[manulActual])

def windowHelp():           # Ventana de ayuda
    global manulActual 
    texto = StringVar()
    manulActual = 0
    top = Toplevel()
    top.overrideredirect(True) # Quitar barra de título
    anchoVentana = 1200         #Definir medidas de ventana
    altoVentana = 700
    xVentana = root.winfo_screenwidth() // 2 - anchoVentana // 2  #Definir posición de la ventana
    yVentana = root.winfo_screenheight() // 2 - altoVentana // 2
    posicion = str(anchoVentana) + "x" + str(altoVentana) + \
        "+" + str(xVentana) + "+" + str(yVentana)
    top.geometry(posicion)
    top.resizable(False, False)    #La ventana no se puede alargar ni ensanchar
    top.config(bg=colorFondo)
    top.title("Ayuda")
    lblImg = Label(top,background=colorFondo,borderwidth=1,width=900,height=520)
    insertarImagen(top,lblImg,texto)
    ttk.Label(top, text="Manual", style="Label.TLabel" ).grid(row=0, column=0,padx = 30,pady=15)
    lblTexto = ttk.Label(top, textvariable=texto, background=colorFondo,foreground=colorFuente,style="Label2.TLabel" )
    lblTexto.grid(row=3, column=0, columnspan=3)
    RoundedButton(top,text="<",ancho=50, radius=10, btnbackground=cuartoColor, btnforeground=colorFondo, clicked=lambda:anteriorImagen(top,lblImg,texto)).grid(row=1, column=0)
    RoundedButton(top,text=">",ancho=50,radius=10, btnbackground=cuartoColor, btnforeground=colorFondo, clicked=lambda:siguienteImagen(top,lblImg,texto)).grid(row=1, column=2)
    RoundedButton(top,text="Cerrar Manual", ancho=200, radius=40, btnbackground="red", btnforeground=colorFuente, clicked=top.destroy).grid(row=4, column=1,sticky='e')

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
        # win = Window()
        # label = tk.Label(win.root, text="Overlay locochon")
        # label.pack()
        # win.launch()
        recognize.init2(currentScene)


    root.withdraw()
    top = Toplevel()
    #top.geometry("900x600")
    #top.geometry("+400+300")
    anchoVentana = 800       #Definir medidas de ventana
    altoVentana = 650
    xVentana = root.winfo_screenwidth() // 2 - anchoVentana // 2  #Definir posición de la ventana
    yVentana = root.winfo_screenheight() // 2 - altoVentana // 2
    posicion = str(anchoVentana) + "x" + str(altoVentana) + \
        "+" + str(xVentana) + "+" + str(yVentana)
    top.title("root nueva")
    top.geometry(posicion)
    top.resizable(False, False)    #La ventana no se puede alargar ni ensanchar
    top.config(bg=colorFondo)
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
            # setDropdown(unusedGest)

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
        
        updateLabels()
        currentScene.saveScene()


    # Boton para el inicio del reconocimiento
    b = RoundedButton(top,text="Iniciar reconocimiento",ancho=260 ,radius=20, btnbackground=cuartoColor, btnforeground="black", clicked=initRecognize)
    b.grid(row=0, column=0,columnspan=2, pady=10)
    # Boton para guardar cambios
    b2 = RoundedButton(top,text="Guardar cambios",ancho=240 , radius=20, btnbackground=quintoColor, btnforeground=colorFuente, clicked=saveScene)
    b2.grid(row=0, column=2,columnspan=2, pady=10)
    # Boton para actualizar etiquetas
    b3 = RoundedButton(top,text="Actualizar",ancho=240 , radius=20, btnbackground=tercerColor, btnforeground=colorFuente, clicked=refreshScene)
    b3.grid(row=0, column=4,columnspan=2, pady=10)

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
                    ("Excel","*.xlsx"),
                    ("Cualquier archivo","*.*")
                ))
            return path
        except Exception as e:
            print("No abriste nada")
            print(e)

    def getLink(gestNum, opt):
        top2 = Toplevel()
        top2.geometry("400x200")
        anchoVentana = 400       #Definir medidas de ventana
        altoVentana = 150
        xVentana = root.winfo_screenwidth() // 2 - anchoVentana // 2  #Definir posición de la ventana
        yVentana = root.winfo_screenheight() // 2 - altoVentana // 2
        posicion = str(anchoVentana) + "x" + str(altoVentana) + \
            "+" + str(xVentana) + "+" + str(yVentana)
        top2.geometry(posicion)
        top2.config(bg=colorFondo)
        top2.resizable(False, False)    #La ventana no se puede alargar ni ensanchar
        top2.title("Ingresa el enlace")

        def close_window():
            global currentScene
            currentScene.updateSceneGestures(2, [gestNum, opt, E.get()])
            top2.destroy()

        E= Entry(top2,width=58)
        E.grid(row=0,padx= 20, pady=20)
        RoundedButton(top2,text="Guardar Enlace",ancho=200 , radius=40, btnbackground=quintoColor, btnforeground=colorFuente, clicked=close_window).grid(row=1)

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
                linkLabel.config(width=15)
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
            

def windowCreateScene():    # Ventana de creacion de escenario
    top = Toplevel(root)
    #top.geometry("400x200")
    #top.geometry("+400+400")
    anchoVentana = 500         #Definir medidas de ventana
    altoVentana = 250
    xVentana = root.winfo_screenwidth() // 2 - anchoVentana // 2  #Definir posición de la ventana
    yVentana = root.winfo_screenheight() // 2 - altoVentana // 2
    posicion = str(anchoVentana) + "x" + str(altoVentana) + \
        "+" + str(xVentana) + "+" + str(yVentana)
    top.geometry(posicion)
    top.resizable(False, False)    #La ventana no se puede alargar ni ensanchar
    top.config(bg=colorFondo)
    top.title("Crear un nuevo escenario")
    # frame2 = Frame(top, bd=5, relief="sunken", padx=20, pady=20).pack()
    lbl1 = ttk.Label(top, text="Nombre del escenario:", style="Label.TLabel")
    lbl1.grid(row=0,column=0)
    lbl2 = ttk.Label(top, text="Fecha de creacion:", style="Label.TLabel")
    lbl2.grid(row=1,column=0)
    
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

    e1 = Entry(top,width=25)
    e1.grid(row=0, column=1, pady=30, padx=20)
    e1.focus()
    lbl3 = ttk.Label(top, text=date.today(), style="Label.TLabel")
    lbl3.grid(row=1, column=1)
    RoundedButton(top,text="Crear Escenario",ancho=240 , radius=40, btnbackground=quintoColor, btnforeground=colorFuente, clicked=sceneCreation).grid(row=2,columnspan=2, column=1,pady=40)

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
"""
archivoMenu = Menu(menuBar, tearoff=0)
ayudaMenu = Menu(menuBar, tearoff=0)

archivoMenu.add_command(label="Nuevo", command=windowCreateScene)
archivoMenu.add_command(label="Abrir", command=openFile)
archivoMenu.add_separator()
archivoMenu.add_command(label="Salir", command=root.quit)

ayudaMenu.add_command(label="Ayuda")

menuBar.add_cascade(label="Archivo", menu=archivoMenu)
menuBar.add_cascade(label="Ayuda", menu=ayudaMenu)
"""
# Configurar la root principal
root.title("RGM OPMA") # Reconocimiento de gestos manuales para la organización y presentación de material audiovisual
#root.geometry("500x300")
#root.geometry("+750+300")
anchoVentana = 580         #Definir medidas de ventana
altoVentana = 380
xVentana = root.winfo_screenwidth() // 2 - anchoVentana // 2  #Definir posición de laventana
yVentana = root.winfo_screenheight() // 2 - altoVentana // 2
posicion = str(anchoVentana) + "x" + str(altoVentana) + \
    "+" + str(xVentana) + "+" + str(yVentana)
root.geometry(posicion)
root.resizable(False,False)
root.config(bg=colorFondo, menu=menuBar)

# Crear un contenido principal
s = ttk.Style()
s.configure('Label.TLabel',
        background = colorFondo,
        foreground = colorFuente,
        font=('Century Gothic', 16))
s2 = ttk.Style()
s2.configure('Label2.TLabel',
        background = colorFondo,
        foreground = colorFuente,
        font=('Century Gothic', 12))
ttk.Label(root, text="Menú principal", style="Label.TLabel").grid(row=0, column=0,pady=20,padx=5)
#label2 = Label(root, text="Abre o crea un nuevo escenario para continuar:", bg=defBG, fg=defFontColor).grid(row=1, column=0,pady=20,padx=20)

RoundedButton(root,text="Abrir/Editar Escenario",ancho=240 , radius=40, btnbackground=tercerColor, btnforeground=colorFuente, clicked=openFile).grid(row=2, column=1,pady=40)
RoundedButton(root,text="Nuevo Escenario",ancho=240 , radius=40, btnbackground=tercerColor, btnforeground=colorFuente, clicked=windowCreateScene).grid(row=3, column=1)


#b2 = Button(root, text="Abrir", command=openFile).grid(row=2, column=0,pady=20,padx=20)
#b3 = Button(root, text="Crear", command=windowCreateScene).grid(row=3, column=0,pady=20,padx=20)
# b4 = Button(root, text="config", command=windowConfigScene).pack()

#b5 = Button(root, text="?", bg=defBG, fg=defFontColor, command=windowHelp).grid(row=0, column=2,pady=20,padx=20)
b5 = RoundedButton(root, text="?",ancho=240 , radius=40,btnbackground=colorFondo, btnforeground=colorFuente, clicked=windowHelp).grid(row=0, column=2)

root.mainloop()