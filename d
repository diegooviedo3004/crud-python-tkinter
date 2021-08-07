def leer():
    Conexion = sqlite3.connect('BBDD')
    Cursero = Conexion.cursor()
    valores = [id_var.get(),Nombre_var.get(),Password_var.get(),Apellidos_var.get(),Direccion_var.get(),textBox.get("1.0",'end')]
    Cursero.execute("SELECT * FROM DATOSUSUARIOS")
    personas = Cursero.fetchall()
   
    valores_string = []
    personas_string = []
   
    for i in range(0,len(valores),1):
        if(valores[i] != '' and valores[i] != '\n'):
            valores_string.append(valores[i])
   
    if(len(valores_string) != 1):
        return messagebox.showerror('Fallo al buscar','Se ha introducido mas de un campo')
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
                    Comentarios_var.insert()
                b = b + 1
            a = a + 1
    Conexion.close()