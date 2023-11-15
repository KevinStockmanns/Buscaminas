import sqlite3 as db
import datetime

con = db.connect("jugadas.db")
cursor = con.cursor()

def crear_tabla():
    cursor.execute("""CREATE TABLE if not exists usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                dificultad TEXT,
                segundos INTEGER,
                fecha DATE
    );""")

def insertar_usuario(nombre, dificultad, tiempo):
    fecha = datetime.date.today()
    cursor.execute("INSERT INTO usuarios(nombre, dificultad, segundos, fecha) VALUES(?, ? , ?, ?)", (nombre.lower(), dificultad, tiempo, fecha))
    usuario_id = cursor.lastrowid
    con.commit()
    return usuario_id

def obtener_datos(dificultad=None):
    datos = []
    if dificultad is None:
        datos = cursor.execute("SELECT * FROM usuarios").fetchall()
    else:
        datos = cursor.execute(f"SELECT * FROM usuarios WHERE dificultad = '{dificultad}' ORDER BY segundos ASC, fecha ASC").fetchall()
    return datos

def usuario_con_nombre(nombre, dificultad):
    datos = cursor.execute(f"SELECT * FROM usuarios WHERE nombre = '{nombre.lower()}' and dificultad = '{dificultad}'").fetchall()
    return (len(datos) > 0)