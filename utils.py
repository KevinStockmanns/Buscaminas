from tkinter import ttk
from tkinter import *
import base_datos as db

def centrar_ventana(ventana, ancho, alto):
    x= (ventana.winfo_screenwidth() - ancho) // 2 
    y= (ventana.winfo_screenheight() - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana.resizable(False, False)

def tiempo_a_seg(tiempo):
    seg = int(tiempo[0:2]) * 60 + int(tiempo[3:5])
    return seg

def format_tiempo(segundos):
    min = str(segundos // 60)
    seg = str(segundos % 60)
    if(len(min) == 1):
        min = f"0{min}"
    if(len(seg) == 1):
        seg = f"0{seg}"
    tiempo = f"{min}:{seg}"
    return tiempo

def calcular_puntaje(segundos):
    puntaje = 100000 // segundos
    return puntaje

def obtener_coordenadas(btn):
    fila = (btn.winfo_y()  // btn.winfo_width())
    columna = (btn.winfo_x()// btn.winfo_width())

    return [fila, columna]

def crear_treeview(tk_puntaje):
    columnas = ('posicion', 'nombre', 'dificultad', 'tiempo', 'score')

    tabla = ttk.Treeview(tk_puntaje, columns=columnas, show='headings')

    tabla.heading('posicion', text='Posición', anchor="center")
    tabla.heading('nombre', text='Nombre', anchor="center")
    tabla.heading('dificultad', text='Dificultad', anchor="center")
    tabla.heading('tiempo', text='Tiempo', anchor="center")
    # tabla.heading('fecha', text='Fecha', anchor="center")
    tabla.heading('score', text='Score', anchor="center")

    ancho_columna = (tk_puntaje.winfo_width()-20) // 5
    tabla.column('posicion', width=ancho_columna)
    tabla.column('nombre', width=ancho_columna)
    tabla.column('dificultad', width=ancho_columna)
    tabla.column('tiempo', width=ancho_columna)
    # tabla.column('fecha', width=ancho_columna)
    tabla.column('score', width=ancho_columna)

    return tabla

def ingresar_datos_treeview(tabla, datos, ventana, distancia_y, id_usuario=None):
    posicion = 1
    max_jugadores = min(10, len(datos))
    for i in range(max_jugadores):
        nombre = datos[i][1].upper()
        dificultad_ = datos[i][2].upper()
        segundos = format_tiempo(datos[i][3])
        # fecha = datos[i][4]
        score = calcular_puntaje(datos[i][3])

        valores = [posicion, nombre, dificultad_, segundos, score]
        tabla.insert('', END, values=valores)
        posicion +=1

    jug = ""
    mej = ""
    if(max_jugadores == 1):
        jug = "jugador"
        mej = "mejor"
    else:
        jug = "jugadores"
        mej = "mejores"
    Label(ventana, text=f"{mej.capitalize()} {max_jugadores} {jug} del nivel {dificultad_}", font=("Arial", 11, "bold")).place(x=10, y=distancia_y-10, width=ventana.winfo_width()-20)

    if not (id_usuario is None):
        contador = 0
        seguir_buscando = True
        while(contador < len(datos) and seguir_buscando):
            if(datos[contador][0] == id_usuario):
                seguir_buscando = False
            contador += 1
        Label(ventana, text=f"Haz ingresado en el puesto número {contador}", bg="#D772FA", fg="white").place(x=10, y=distancia_y+10, width=ventana.winfo_width()-20)
    # Label(ventana, text=f"Haz ingresado en el puesto número {1}").place(x=10, y=10, width=ventana.winfo_width())

    tabla.place(x=10, y=distancia_y+30, width=ventana.winfo_width()-20, height=160)