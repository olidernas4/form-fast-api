from fastapi import FastAPI, HTTPException  # FastAPI = crear API, HTTPException = lanzar errores (400/404)
from pydantic import BaseModel, EmailStr  # BaseModel = valida JSON, EmailStr = valida formato de email

from db import get_conn  # get_conn() abre una conexión a PostgreSQL


app = FastAPI(title="Mi API (CRUD sencillo)")  # crea la aplicación (servidor web)


# Modelo para el BODY del POST (crear)
class FormularioCreate(BaseModel):
    nombre: str  # requerido
    apellido: str  # requerido
    email: EmailStr | None = None  # opcional (valida formato email)
    edad: int | None = None  # opcional (entero)
    peso: float | None = None  # opcional (decimal)
    genero: str | None = None  # opcional (1 caracter: 'M' o 'F')


# Modelo para el BODY del PUT (editar): todo opcional
class FormularioUpdate(BaseModel):
    nombre: str | None = None  # opcional (solo mandas lo que quieres cambiar)
    apellido: str | None = None
    email: EmailStr | None = None
    edad: int | None = None
    peso: float | None = None
    genero: str | None = None


# Ruta raíz solo para probar que el servidor funciona
@app.get("/")  # método HTTP GET
def inicio():
    return {"mensaje": "hola mundo", "docs": "/docs"}  # devuelve JSON (dict de Python)


# CREATE: crear un registro en la tabla (INSERT)
@app.post("/formularios", status_code=201)  # 201 = creado
def crear_formulario(data: FormularioCreate):
    # Si genero viene, debe ser 1 caracter (porque la columna es CHAR(1))
    if data.genero is not None and len(data.genero) != 1:  # validación
        raise HTTPException(status_code=400, detail="genero debe tener 1 caracter")  # 400 = error del usuario

    with get_conn() as conn:  # abre conexión a la BD
        with conn.cursor() as cur:  # crea un cursor para ejecutar SQL
            cur.execute(  # ejecuta SQL usando parámetros (%s)
                """
                INSERT INTO formularios (nombre, apellido, email, edad, peso, genero)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (data.nombre, data.apellido, data.email, data.edad, data.peso, data.genero),
            )
            new_id = cur.fetchone()[0]  # fetchone() trae 1 fila: (id,) y tomamos el id con [0]

    return {"id": new_id, **data.model_dump()}  # respuesta JSON con los datos + id


# READ: listar registros (SELECT *)
@app.get("/formularios")
def listar_formularios():
    with get_conn() as conn:  # abre conexión
        with conn.cursor() as cur:  # cursor para SQL
            cur.execute(
                """
                SELECT id, nombre, apellido, email, edad, peso, genero, creado_en
                FROM formularios
                ORDER BY id DESC
                """
            )
            rows = cur.fetchall()  # lista de filas

    # `rows` es una lista de tuplas, por ejemplo:
    # [
    #   (3, 'Ana', 'Gómez', 'ana@mail.com', 30, 60.2, 'F', datetime...),
    #   (2, 'Juan', 'Pérez', 'juan@mail.com', 25, 70.5, 'M', datetime...),
    # ]
    #
    # Ahora convertimos cada tupla (fila) en un diccionario (JSON) para devolverlo en la API.
    resultados = []  # aquí iremos guardando cada registro convertido a dict
    for r in rows:  # r = una fila (tupla) en el mismo orden del SELECT
        resultados.append(
            {
                "id": r[0],  # columna 1 del SELECT
                "nombre": r[1],  # columna 2 del SELECT
                "apellido": r[2],  # columna 3 del SELECT
                "email": r[3],  # columna 4 del SELECT
                "edad": r[4],  # columna 5 del SELECT
                "peso": r[5],  # columna 6 del SELECT
                "genero": r[6],  # columna 7 del SELECT
                "creado_en": r[7],  # columna 8 del SELECT
            }
        )

    return resultados  # FastAPI lo convierte a JSON automáticamente


# READ: información rápida (ej: contar filas)
@app.get("/formularios/info")
def info_formularios():
    # Este endpoint sirve para ver información rápida de la tabla.
    # En este caso, cuenta cuántos registros (filas) hay en `formularios`.

    with get_conn() as conn:  # abre conexión a PostgreSQL
        with conn.cursor() as cur:  # cursor para ejecutar SQL
            cur.execute("SELECT COUNT(*) FROM formularios")  # SQL: cuenta cuántas filas hay
            total = cur.fetchone()[0]  # resultado viene como (total,) y total está en la posición [0]

    return {"total": total}  # FastAPI lo devuelve como JSON: {"total": 3}


# READ: obtener 1 registro por id (SELECT ... WHERE id = ?)
@app.get("/formularios/{form_id}")  # {form_id} es un parámetro en la URL
def obtener_formulario(form_id: int):
    # ejemplo de URL: /formularios/10  => form_id = 10
    with get_conn() as conn:  # abre conexión
        with conn.cursor() as cur:  # cursor para SQL
            cur.execute(  # consulta 1 registro
                """
                SELECT id, nombre, apellido, email, edad, peso, genero, creado_en
                FROM formularios
                WHERE id = %s
                """,
                (form_id,),  # el valor que reemplaza el %s
            )
            r = cur.fetchone()  # una sola fila
    if not r:
        raise HTTPException(status_code=404, detail="No existe")  # 404 si no encuentra
    return {
        "id": r[0],  # columna 1 del SELECT
        "nombre": r[1],  # columna 2
        "apellido": r[2],  # columna 3
        "email": r[3],  # columna 4
        "edad": r[4],  # columna 5
        "peso": r[5],  # columna 6
        "genero": r[6],  # columna 7
        "creado_en": r[7],  # columna 8
    }


# UPDATE: editar un registro por id (UPDATE ... WHERE id = ?)
@app.put("/formularios/{form_id}")
def actualizar_formulario(form_id: int, data: FormularioUpdate):
    if data.genero is not None and len(data.genero) != 1:
        raise HTTPException(status_code=400, detail="genero debe tener 1 caracter")
    values = data.model_dump(exclude_unset=True)  # solo campos que el usuario envió en el JSON
    if not values:
        return {"mensaje": "Nada para actualizar"}
    allowed = {"nombre", "apellido", "email", "edad", "peso", "genero"}  # campos permitidos
    set_parts, params = [], []  # partes del SET y valores para %s
    for key, value in values.items():
        if key in allowed:
            set_parts.append(f"{key} = %s")  # ejemplo: "edad = %s"
            params.append(value)  # valor real
    params.append(form_id)  # el id va al final porque el SQL termina en "WHERE id = %s"
    with get_conn() as conn:  # abre conexión
        with conn.cursor() as cur:  # cursor para SQL
            cur.execute(
                f"UPDATE formularios SET {', '.join(set_parts)} WHERE id = %s",
                tuple(params),
            )
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="No existe")  # no se actualizó nada => id no existe
    return {"mensaje": "Actualizado", "id": form_id, **values}


# DELETE: eliminar un registro por id (DELETE ... WHERE id = ?)
@app.delete("/formularios/{form_id}")
def eliminar_formulario(form_id: int):
    with get_conn() as conn:  # abre conexión
        with conn.cursor() as cur:  # cursor para SQL
            cur.execute("DELETE FROM formularios WHERE id = %s", (form_id,))  # elimina por id
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="No existe")  # si no borró nada, el id no existe
    return {"mensaje": "Eliminado", "id": form_id}  # respuesta final
