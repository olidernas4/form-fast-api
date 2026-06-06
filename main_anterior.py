from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def incio():
    return {"mensaje": "hola mundo"}


@app.get("/usuarios")
def obtener_usuarios():
    return ["juan", "andres", "ana"]


# select * from usuarios;


@app.get("/usuarios/{id}")
def obtener_usuario(id: int):
    return {"usuario_id": id}

    # post crear datos
    # put para actualizar datos
    # delete para eliminar datos
    # get obtener datos consultar


###################################################################  post #############################################
@app.post("usuarios_add")
def crear_usuario(nombre: str):
    return {"mensaje": f"usuario {nombre} creado"}


# INSERT INTO usuarios (nombre) values ("juan")


####################### ################### PUT #######################################################################
@app.put("/usuarios_update/{id}")
def actualizar_usuario(id: int, nombre: str):
    return {"mensaje": f"usuario {id}  actualizado el {nombre}"}


# update usuarios set nombre = 'pedro'
# where id = 1;


# post -> es crear
# put -> actualizar

########################################## DELETE ###################################################################
@app.delete("/usuarios/{id}")
def eliminar_usuario(id: int):
    return {"mensaje": f"usuario {id} eliminado"}


# DELETE FROM usuarios where id = 1
@app.delete("/productos/{id}")
def eliminar_producto(id: int):
    return {"mensaje": f"el producto {id} fue  eliminado"}


##################################################### CRUD ###################################################################

# c -> CREATE crear
# r -> READ LEE
# U -> UPDATE ACTUALIZAR
# D -> DELETE ELMINAR

# operacion   significado  http  postgresql
# create        crear       post  insert
# read          leer        GET   SELECT
# update        actualizar   PUT  UPDATE
# delete         elimninar   DELETE DELETE

# EJERCICIO
# 1. CREAR TAREA POST
# 2. VER TAREAS
# 3. EDITAR TAREA
# 4. ELIMINAR UNA TAREA

