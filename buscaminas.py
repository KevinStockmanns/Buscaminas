# Stockmanns Kevin Fabián
from tkinter import * 
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import ttk
import utils
import random
import base_datos as db


def juego(dificultad_elegida):
    global tablero_logico, columnas, filas, minas, frame, tk_main, dificultad
    
    dificultad = dificultad_elegida
    if(dificultad_elegida == "fácil"):
        minas = 15
        filas = 10
        columnas = 10
    elif(dificultad_elegida == "intermedio"):
        minas = 30
        filas = 13
        columnas = 13
    else:
        minas = 60
        filas = 15
        columnas = 15

    # crear el tablero logico sin minas
    for f in range(filas):
        fila = []
        for c in range(columnas):
            fila.append(False)
        tablero_logico.append(fila)


    # cambio de ventana 

    if not tk_inicio is None:
        tk_inicio.destroy()
    tk_main = Tk()
    tk_main.title("Buscaminas")
    utils.centrar_ventana(tk_main, ancho=410, alto=470)
    tk_main.update()

    lbl_cargando = Label(tk_main, name="lbl_cargando", text="Generando Tablero...", font=("Arial", 12, "bold"))
    lbl_cargando.place(x=(tk_main.winfo_width()-200)/2, y=23, width=200)


    frame = Frame(tk_main, bg="light grey")
    frame.place(x=10, y=70, width=390, height=390)
    frame.update()

    generar_tablero()

def generar_tablero():
    global tablero_logico, columnas, imagen_tk_bandera, imagen_tk_mina, frame, dificultad

    dimensiones = 0
    cuadro_ancho = frame.winfo_width() // columnas
    if(dificultad == "fácil"):
        dimensiones = cuadro_ancho//2
    else:
        dimensiones = cuadro_ancho
    
    imagen_tk_bandera = PhotoImage(file="assets/images/bandera.png").subsample(dimensiones, dimensiones)
    imagen_tk_mina = PhotoImage(file="assets/images/mina.png").subsample(dimensiones, dimensiones)
    imagen_tk_reload = PhotoImage(file="assets/images/reload.png").subsample(50//3, 50//3)
    imagen_tk_home = PhotoImage(file="assets/images/home.png").subsample(50//2, 50//2)

    # insertar los botones
    fila = 0
    while(fila < len(tablero_logico)):
        distancia_y = cuadro_ancho * fila
        columna = 0
        while(columna < len(tablero_logico[fila])):
            distancia_x = cuadro_ancho * columna
            btn_cuadro = Button(frame, borderwidth=5)
            btn_cuadro.configure(command=lambda b=btn_cuadro: realizar_jugada(b, frame))
            btn_cuadro.bind("<Button-3>", control_banderas)
            btn_cuadro.place(x=distancia_x, y=distancia_y, width=cuadro_ancho, height=cuadro_ancho)
            columna += 1
        fila += 1
        columna = 0

    tk_main.nametowidget("lbl_cargando").destroy()
    lbl_minas = Label(tk_main, text=minas, bg="black", fg="red", font=("Arial", 25), name="lbl_minas")
    lbl_minas.place(x=10, y=10, width=50, height=50)

    lbl_temp = Label(tk_main, text="00:00", bg="black", fg="red", font=("Arial", 25), name="lbl_temp")
    lbl_temp.place(x=tk_main.winfo_width()-110, y=10, width=100, height=50)

    btn_reload = Button(tk_main, image=imagen_tk_reload, command=reiniciar_partida, name="btn_reload")
    btn_reload.image = imagen_tk_reload
    btn_reload.place(x=130, y=10, width=50, height=50)

    btn_home = Button(tk_main, image=imagen_tk_home, command=pantalla_inicio)
    btn_home.image = imagen_tk_home
    btn_home.place(x=190, y=10, width=50, height=50)
  
def realizar_jugada(btn_cuadrito, frame):
    global tablero_logico, minas, columnas, filas, primerJugada
    coor = utils.obtener_coordenadas(btn_cuadrito)
    fila_seleccionada = coor[0]
    columna_seleccionada = coor[1]
    cuadro_ancho = btn_cuadrito.winfo_width()

    if(primerJugada):
        primerJugada = False
        con_minas = 0

        control_temporizador()

        # Plantar Minas
        while (con_minas < minas):
            a = random.randint(0, filas-1)
            b = random.randint(0, columnas-1)
            if((columna_seleccionada != b and fila_seleccionada != a) and tablero_logico[a][b] == False):
                tablero_logico[a][b] = True
                con_minas += 1

        # Eliminar varios botones cercanos
        for btn in frame.winfo_children():
            
            fila_adyacente= utils.obtener_coordenadas(btn)[0]
            col_adyacente = utils.obtener_coordenadas(btn)[1]
            if ((abs(fila_seleccionada - fila_adyacente) <= 1 and abs(columna_seleccionada - col_adyacente) <= 1)):
                if(tablero_logico[fila_adyacente][col_adyacente] == False):
                    contar_minas_adyacentes(btn, frame, fila_adyacente, col_adyacente)
                    btn.destroy()

    else:
        if(tablero_logico[fila_seleccionada][columna_seleccionada]):


            for i in range(len(tablero_logico)):
                for j in range(len(tablero_logico[i])):
                    if(tablero_logico[i][j]):
                        lbl_btn = Label(frame, bg="red", image=imagen_tk_mina)
                        lbl_btn.image = imagen_tk_mina
                        lbl_btn.place(x=cuadro_ancho*j, y=cuadro_ancho*i, width=cuadro_ancho, height=cuadro_ancho)
            
            terminar_partida(False)
        else:
            contar_minas_adyacentes(btn_cuadrito, frame, fila_seleccionada, columna_seleccionada)
            btn_cuadrito.destroy()

def contar_minas_adyacentes(btn, frame, fila, columna):
    global tablero_logico

    minas_adyacentes = 0
    fila_con = 0
    while(fila_con < len(tablero_logico)):
        col_con = 0
        while(col_con < len(tablero_logico[fila_con])):
            if(abs(fila-fila_con) <= 1 and abs(columna-col_con) <= 1):
                if(tablero_logico[fila_con][col_con]):
                    minas_adyacentes += 1
            col_con += 1
        fila_con += 1
            

    if(minas_adyacentes > 0):
        Label(frame, text=minas_adyacentes, bg="light gray").place(x=btn.winfo_x(), y=btn.winfo_y(), width=btn.winfo_width(), height=btn.winfo_width())

def control_banderas(e):
    global minas, tablero_logico, coordenadas_banderas, imagen_tk_bandera, primerJugada
    btn = e.widget

    fila = utils.obtener_coordenadas(btn)[0]
    columna = utils.obtener_coordenadas(btn)[1]

    tiene_bandera = [fila, columna] in coordenadas_banderas

    if(not tiene_bandera and len(coordenadas_banderas) < minas and (ganador is None) and not primerJugada):
        btn_bandera = Button(frame, image=imagen_tk_bandera, bg="green")
        btn_bandera.image = imagen_tk_bandera
        btn_bandera.bind("<Button-1>", control_banderas)
        btn_bandera.bind("<Button-3>", control_banderas)
        btn_bandera.place(x=btn.winfo_x(), y=btn.winfo_y(), width=btn.winfo_width(), height=btn.winfo_height())
        coordenadas_banderas.append([fila, columna])
        botones_banderas.append(btn_bandera)

    elif(tiene_bandera and ganador is None):
        indice = None
        for i in range(len(coordenadas_banderas)):
            if([fila, columna] == coordenadas_banderas[i]):
                indice = i
        
        botones_banderas[indice].destroy()
        botones_banderas.pop(indice)
        coordenadas_banderas.pop(indice)
    
    if(len(coordenadas_banderas) >= minas):
        gano = True
        for coor in coordenadas_banderas:
            fil = coor[0]
            col = coor[1]
            if tablero_logico[fil][col] == False:
                gano = False

        if (gano):
            terminar_partida(True)
        
    tk_main.nametowidget("lbl_minas").configure(text=minas-len(botones_banderas))

def terminar_partida(gano):
    global frame, ganador, tk_inicio, tk_main
    ganador = gano
    for i in frame.winfo_children():
        i.configure(state="disabled")

    mensaje = ""
    volver_jugar = None
    if(ganador):
        nombre = StringVar()
        pedir_datos = Toplevel(tk_main)
        pedir_datos.title("Ingresa tus Datos")
        utils.centrar_ventana(pedir_datos, 300, 170)
        pedir_datos.update()
        pedir_datos.resizable(False, True)
        Label(pedir_datos, text=f"¡Felicidades! Haz ganado en un tiempo de {temporizador}.\n Ahora por favor ingresa tus datos para ver los puntajes.", wraplength=pedir_datos.winfo_width()-20).place(x=10, y=10)
        Label(pedir_datos, text="Nombre:").place(x=10, y=80)
        Entry(pedir_datos, textvariable=nombre).place(x=70, y=80, width=pedir_datos.winfo_width()-70-20)
        Button(pedir_datos, text="Cargar", command=lambda: cargar_datos(nombre, pedir_datos)).place(x=(pedir_datos.winfo_width()-100)//2, y=110, width=100)
        lbl_error = Label(pedir_datos, text="", fg="red", name="lbl_error")
        lbl_error.place(x=10, y=140, width=pedir_datos.winfo_width()-20)

def cargar_datos(nombre, top_level):
    global dificultad, temporizador, tk_main
    nombre = nombre.get().strip()

    error = ""
    if(len(nombre) < 3 or len(nombre) > 15):
        error = "El nombre debe tener entre 3 y 15 caracteres."
    elif(nombre.isnumeric()):
        error = "El nombre no puede ser algun número."
    elif(db.usuario_con_nombre(nombre, dificultad)):
        error = "El nombre ya esta en uso en esta categoría."
    
    if(error != ""):
        top_level.nametowidget("lbl_error").configure(text=error)
    else:
        id_usuario = db.insertar_usuario(nombre, dificultad, utils.tiempo_a_seg(temporizador))
        top_level.destroy()
        pantalla_puntos(tk_main, id_usuario)

def pantalla_puntos(ventana, id_usuario=None):
    global dificultad
    tk_puntaje = Toplevel(ventana)
    tk_puntaje.title("Puntajes de Jugadores")
    
    datos = db.obtener_datos()

    if(len(datos) > 0):
        distancias_y = [10, 220, 440]
        indice = 0
        if(ventana == tk_inicio):
            utils.centrar_ventana(tk_puntaje, alto=650, ancho=450)
            tk_puntaje.update() 


            datos_facil = db.obtener_datos("fácil")
            if(len(datos_facil) > 0):
                tabla = utils.crear_treeview(tk_puntaje)
                utils.ingresar_datos_treeview(tabla, datos_facil, tk_puntaje, distancias_y[indice])
                indice+=1
            
            datos_intermedio = db.obtener_datos("intermedio")
            if(len(datos_intermedio) > 0):
                tabla = utils.crear_treeview(tk_puntaje)
                utils.ingresar_datos_treeview(tabla, datos_intermedio, tk_puntaje, distancias_y[indice])
                indice+=1

            datos_dificil = db.obtener_datos("difícil")
            if(len(datos_dificil) > 0):
                tabla = utils.crear_treeview(tk_puntaje)
                utils.ingresar_datos_treeview(tabla, datos_dificil, tk_puntaje, distancias_y[indice])
        else:
            utils.centrar_ventana(tk_puntaje, 450, distancias_y[1])
            tk_puntaje.update()
            
            datos_dif_actual = db.obtener_datos(dificultad)
            tabla = utils.crear_treeview(tk_puntaje)
            utils.ingresar_datos_treeview(tabla, datos_dif_actual, tk_puntaje, distancias_y[indice], id_usuario)
            indice +=1
        utils.centrar_ventana(tk_puntaje, 450, distancias_y[indice])
    else:
        utils.centrar_ventana(tk_puntaje, alto=200, ancho=450)
        tk_puntaje.update() 

        Label(tk_puntaje, text="No existen datos cargados\n hasta el momento.", font=("Arial", 12)).place(x=10, y=(tk_puntaje.winfo_height()-20-24)//2, width=tk_puntaje.winfo_width()-20)

    tk_puntaje.update_idletasks()

def control_temporizador():
    global temporizador, ganador, referencia_after
    if (ganador is None):
        segundos = utils.tiempo_a_seg(temporizador)
        segundos += 1
        
        temporizador = utils.format_tiempo(segundos)

        lbl_temp = tk_main.nametowidget("lbl_temp")
        lbl_temp.config(text=temporizador)
        referencia_after = tk_main.after(1000, control_temporizador)
  
def pantalla_inicio():
    global tablero_logico, coordenadas_banderas, botones_banderas, tk_main, frame, columnas, filas, minas, primerJugada, temporizador, ganador, referencia_after, tk_inicio

    # Reinicio de las variables necesarias
    tablero_logico = []
    coordenadas_banderas = []
    botones_banderas = []
    if not (referencia_after is None):
        tk_main.after_cancel(referencia_after)
    referencia_after = None
    temporizador = "00:00"

    if not tk_main is None:
        tk_main.destroy()
    tk_main = None
    frame = None
    primerJugada = True
    ganador = None

    tk_inicio = Tk()
    tk_inicio.title("Buscaminas")
    utils.centrar_ventana(tk_inicio, ancho=450, alto=340)
    tk_inicio.configure(bg="light grey")
    tk_inicio.update()

    Label(tk_inicio, text="BUSCAMINAS", bg="light grey", font=("Arial", 35)).place(x=0, y=30, width=tk_inicio.winfo_width())

    Label(tk_inicio, text="Elige un nivel de dificultad", bg="light grey", font=("Arial", 12)).place(x=0, y=100, width=tk_inicio.winfo_width())

    Button(tk_inicio, text="Fácil", bg="light grey", font=("Arial", 15), command=lambda: juego("fácil")).place(x=(tk_inicio.winfo_width() - 150) // 2, y=150, width=150)
    Button(tk_inicio, text="Intermedio", bg="light grey", font=("Arial", 15), command=lambda: juego("intermedio")).place(x=(tk_inicio.winfo_width() - 150) // 2, y=200, width=150)
    Button(tk_inicio, text="Difícil", bg="light grey", font=("Arial", 15), command=lambda: juego("difícil")).place(x=(tk_inicio.winfo_width() - 150) // 2, y=250, width=150)

    Button(tk_inicio, text="Ver Puntajes", command=lambda: pantalla_puntos(tk_inicio), bg="light grey").place(x=tk_inicio.winfo_width()-100-5, y=tk_inicio.winfo_height()-20-10, width=100)

    # tk_inicio = tk_inicio
    return tk_inicio

def reiniciar_partida():
    global tk_main, frame, primerJugada, temporizador, ganador, tablero_logico, coordenadas_banderas, botones_banderas, tk_inicio, dificultad, referencia_after

    # Reinicio de variables necesarias
    tablero_logico = []
    coordenadas_banderas = []
    botones_banderas = []
    if not (referencia_after is None):
        tk_main.after_cancel(referencia_after)
    referencia_after = None
    temporizador = "00:00"
    tk_main.destroy()
    tk_main = None
    frame = None
    primerJugada = True
    ganador = None
    tk_inicio = None

    # Volver a abrir la ventana de la misma dificultad
    juego(dificultad)
    

tablero_logico = []
coordenadas_banderas = []
botones_banderas = []
tk_main = None
frame = None
dificultad = None
columnas = 0
filas = 0
minas = 0
primerJugada = True
temporizador = "00:00"
referencia_after = None
ganador = None
imagen_tk_bandera = None
imagen_tk_mina = None

db.crear_tabla()

tk_inicio = pantalla_inicio()

tk_inicio.mainloop()