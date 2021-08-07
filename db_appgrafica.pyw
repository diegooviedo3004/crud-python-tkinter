from sqlite3.dbapi2 import IntegrityError, connect
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import sqlite3
import os.path
import string

ventana = Tk()
ventana.title("CRUD")
ventana.geometry("300x350")

# TO USE THE WHOLE SPACE WE GOTTA ADD THE COLUMNS NUMBER
ventana.columnconfigure(0, weight=1)
ventana.columnconfigure(1, weight=1)
ventana.columnconfigure(2, weight=1)
ventana.columnconfigure(3, weight=1)

# STRING AND STUFF VARIABLES

id_var = StringVar()
Nombre_var = StringVar()
Password_var = StringVar()
Apellidos_var = StringVar()
Direccion_var = StringVar()
Comentarios_var = StringVar()

# ------------------------------CLASSES


class Texto():
    def __init__(self, texto, fila) -> None:
        self = Label(ventana)
        self.configure(text=texto, justify='center', padx=10, pady=10)
        self.grid(row=fila, columnspan=2, column=0)


class Entrada():
    def __init__(self, fila, textvar) -> None:
        self = Entry(ventana)
        self.configure(textvariable=textvar)
        self.grid(row=fila, columnspan=2, column=2, padx=10)


class Boton():
    def __init__(self, fila, columna, texto, comando) -> None:
        self = Button(ventana)
        self.configure(text=texto, padx=5, pady=3, command=comando)
        self.grid(column=columna, row=fila, pady=20)


def salir():
    respuesta = messagebox.askokcancel(
        'Salir', 'Presione Ok para salir del CRUD')
    if(respuesta):
        ventana.destroy()


def conectar():
    if(os.path.isfile('BBDD') == False):
        Conexion = sqlite3.connect('BBDD')
        Puntero = Conexion.cursor()
        Puntero.execute('''
        CREATE TABLE DATOSUSUARIOS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NOMBRE_USUARIO VARCHAR(50),
            PASSWORD VARCHAR(50),
            APELLIDOS VARCHAR(50),
            DIRECCION VARCHAR(50),
            COMENTARIOS VARCHAR(300)

        )
        ''')
        Conexion.close()
    else:
        return messagebox.showerror('Fallo al crear Base de Datos', 'La base de datos ya existe')


def borrartodoscampos():
    id_var.set("")
    Nombre_var.set("")
    Password_var.set("")
    Apellidos_var.set("")
    Direccion_var.set("")
    textBox.delete("1.0", "end")


def crear():
    Conexion = sqlite3.connect('BBDD')
    Cursero = Conexion.cursor()
    valores = (id_var.get(), Nombre_var.get(), Password_var.get(
    ), Apellidos_var.get(), Direccion_var.get(), textBox.get("1.0", 'end'))
    try:
        Cursero.execute(
            "INSERT INTO DATOSUSUARIOS VALUES (?,?,?,?,?,?)", valores)
        messagebox.showinfo('Crear', 'Su usuario fue ingresado exitosamente')
    except IntegrityError:
        return messagebox.showerror('Fallo al crear el usuario', 'ID incorrecto')

    Conexion.commit()
    Conexion.close()


def leer():
    Conexion = sqlite3.connect('BBDD')
    Cursero = Conexion.cursor()
    valores = [id_var.get(), Nombre_var.get(), Password_var.get(
    ), Apellidos_var.get(), Direccion_var.get(), textBox.get("1.0", 'end')]
    Cursero.execute("SELECT * FROM DATOSUSUARIOS")
    personas = Cursero.fetchall()

    valores_string = []

    for i in range(0, len(valores), 1):
        if(valores[i] != '' and valores[i] != '\n'):
            valores_string.append(valores[i])

    if(len(valores_string) != 1):
        return messagebox.showerror('Fallo al buscar', 'Se ha introducido mas de un campo')
    else:
        a = 0
        b = 0
        for i in personas:
            for j in i:
                if(str(j) == valores_string[0]):
                    id_var.set(personas[a][0])
                    Nombre_var.set(personas[a][1])
                    Password_var.set(personas[a][2])
                    Apellidos_var.set(personas[a][3])
                    Direccion_var.set(personas[a][4])
                    textBox.insert('1.0', personas[a][5])
                b = b + 1
            a = a + 1
    Conexion.close()


def actualizar():
    Conexion = sqlite3.connect('BBDD')
    Cursero = Conexion.cursor()
    updating = '''
        UPDATE DATOSUSUARIOS SET NOMBRE_USUARIO = ?, PASSWORD = ?, APELLIDOS = ?, DIRECCION = ?, COMENTARIOS = ? WHERE ID = ?
    '''
    valores = (Nombre_var.get(),Password_var.get(),Apellidos_var.get(),Direccion_var.get(),textBox.get("1.0", 'end'),id_var.get())
    Cursero.execute(updating,valores)
    Conexion.commit()
    Cursero.close()
    Conexion.close()
    return messagebox.showinfo('Actualizar','Se han actualizado los campos correspondientes')

def borrar():
   Conexion = sqlite3.connect('BBDD')
   Cursero = Conexion.cursor() 
   updating = "DELETE FROM DATOSUSUARIOS WHERE ID = ?"
   valor = (id_var.get())
   Cursero.execute(updating,valor)
   Conexion.commit()
   Cursero.close()
   Conexion.close()
   return messagebox.showinfo('Borrar','Se ha eliminado el registro de la base de datos')


# ---------------------------MENU


barramenu = Menu(ventana)
ventana.config(menu=barramenu)


# CREATING THE PARTS OF THE MAINS

archivoBBDD = Menu(barramenu, tearoff=0)
archivoBorrar = Menu(barramenu, tearoff=0)
archivoCRUD = Menu(barramenu, tearoff=0)
archivoAyuda = Menu(barramenu, tearoff=0)

# FIRST SUBPARTS

archivoBBDD.add_command(label='Conectar', command=conectar)
archivoBBDD.add_separator()
archivoBBDD.add_command(label='Salir', command=salir)

# SECOND SUBPARTS

archivoBorrar.add_command(label='Borrar campos', command=borrartodoscampos)

# THIRD SUBPARTS

archivoCRUD.add_command(label='Crear', command=crear)
archivoCRUD.add_command(label='Leer', command=leer)
archivoCRUD.add_command(label='Actualizar', command=actualizar)
archivoCRUD.add_command(label='Borrar',command=borrar)

# FOURTH SUBPARTS

archivoAyuda.add_command(label='Licencia')
archivoAyuda.add_command(label='Acerca de')

# CREATING MAIN MENU PARTS
barramenu.add_cascade(label="BBDD", menu=archivoBBDD)
barramenu.add_cascade(label="Borrar", menu=archivoBorrar)
barramenu.add_cascade(label="CRUD", menu=archivoCRUD)
barramenu.add_cascade(label="Ayuda", menu=archivoAyuda)


# ---------------------------------
id_ = Texto('ID', 0)
Nombre = Texto('Nombre', 1)
Password = Texto('Password', 2)
Apellido = Texto('Apellido', 3)
Direccion = Texto('Direccion', 4)
Comentarios = Texto('Comentarios', 5)

EntradaID = Entrada(0, id_var)
EntradaNombre = Entrada(1, Nombre_var)
EntradaPassword = Entrada(2, Password_var)
EntradaApellido = Entrada(3, Apellidos_var)
EntradaDireccion = Entrada(4, Direccion_var)

# CREATING THE SCROLL PLACE FOR THE COMENTS

textBox = ScrolledText(ventana, width=13, height=5)
textBox.grid(row=5, column=2, columnspan=2)

# CREATING BUTTONS

Crear = Boton(6, 0, 'Crear', crear)
Leer = Boton(6, 1, 'Leer', leer)
Actualizar = Boton(6, 2, 'Actualizar', actualizar)
Borrar = Boton(6, 3, 'Borrar', borrar)


ventana.mainloop()
