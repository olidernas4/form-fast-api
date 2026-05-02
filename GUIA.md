# Guía rápida (sin tokens) – FastAPI + PostgreSQL

## 1) SQL: crear BD, tabla y datos

Archivo: `sql/postgres_formulario.sql`

- `CREATE DATABASE mi_form_db;` crea la base de datos.
- `CREATE TABLE ... formularios (...)` crea la tabla con campos:
  - `id SERIAL`: número que se auto-incrementa.
  - `nombre VARCHAR(100)`: texto variable (hasta 100).
  - `genero CHAR(1)`: texto fijo de 1 caracter.
  - `edad INT`: entero.
  - `peso FLOAT`: decimal.
- `INSERT INTO ...` agrega 3 registros de ejemplo.

Ejecutarlo con `psql` (ejemplo):
- Conéctate a postgres y corre el archivo.
- Luego conéctate a la BD `mi_form_db`.

## 2) Conexión a la base de datos (sencillo)

Archivo: `db.py`

Líneas / idea:
- `import os`: lee variables de entorno.
- `_conn_params()`: arma los datos de conexión (host, user, password, dbname).
- `get_conn()`: abre conexión, hace `commit` si todo bien, o `rollback` si hay error, y siempre cierra.

Valores por defecto (para aprender):
- host: `localhost`
- port: `5432`
- user: `postgres`
- password: `postgres` (cámbialo por el tuyo)
- db: `mi_form_db`

Si tu password NO es `postgres`, cambia con PowerShell:
- `$env:PGPASSWORD="TU_PASSWORD"`

También puedes cambiar:
- `$env:PGHOST="localhost"`
- `$env:PGPORT="5432"`
- `$env:PGUSER="postgres"`
- `$env:PGDATABASE="mi_form_db"`

## 3) CRUD (crear / ver / editar / eliminar)

Archivo: `main.py`

Explicación (línea por línea, por bloques):

### Imports
- `from fastapi import FastAPI, HTTPException`: crea la app y permite responder errores con código (400/404).
- `from pydantic import BaseModel, EmailStr`: valida JSON de entrada (ej: email válido).
- `from db import get_conn`: trae la función para conectarse a PostgreSQL.

### App
- `app = FastAPI(...)`: crea tu API.

### Modelos (lo que mandas en Postman)
- `class FormularioCreate(BaseModel)`: define campos para CREAR (POST).
- `class FormularioUpdate(BaseModel)`: define campos para EDITAR (PUT). Todos opcionales.

### Endpoint: crear (POST /formularios)
- `@app.post("/formularios", ...)`: ruta + método POST.
- `def crear_formulario(data: FormularioCreate)`: recibe JSON y lo valida.
- `with get_conn() as conn`: abre conexión (y al final hace commit/cierra).
- `cur.execute(... INSERT ...)`: inserta en la tabla.
- `RETURNING id`: PostgreSQL devuelve el id creado.

### Endpoint: listar (GET /formularios)
- `@app.get("/formularios")`: ruta + método GET.
- `cur.execute(... SELECT ...)`: consulta todos los registros.
- `rows = cur.fetchall()`: trae una lista de filas.
- `return [...]`: convierte filas a JSON.

### Endpoint: ver 1 (GET /formularios/{id})
- `@app.get("/formularios/{form_id}")`: ruta con parámetro.
- `form_id: int`: FastAPI convierte a int.
- `cur.fetchone()`: trae 1 fila.
- `if not r: raise HTTPException(404, ...)`: si no existe, devuelve 404.

### Endpoint: editar (PUT /formularios/{id})
- `@app.put(...)`: ruta + método PUT.
- `values = data.model_dump(exclude_unset=True)`: solo toma campos que enviaste.
- `set_parts.append("campo = %s")`: arma el SQL UPDATE dinámico.
- `cur.rowcount`: si es 0, no actualizó nada (no existe).

### Endpoint: eliminar (DELETE /formularios/{id})
- `@app.delete(...)`: ruta + método DELETE.
- `DELETE FROM formularios WHERE id = %s`: elimina el registro.
- `if cur.rowcount == 0`: si no existe, devuelve 404.

## 4) Rutas para Postman (ejemplos)

Base URL (si corres local):
- `http://127.0.0.1:8000`

### Crear (POST)
- URL: `POST /formularios`
- Body (raw JSON):
```json
{
  "nombre": "Carlos",
  "apellido": "Ruiz",
  "email": "carlos@mail.com",
  "edad": 28,
  "peso": 75.5,
  "genero": "M"
}
```

### Ver todos (GET)
- URL: `GET /formularios`

### Info (GET) (cuántos registros hay)
- URL: `GET /formularios/info`

### Ver uno (GET)
- URL: `GET /formularios/1`

### Editar (PUT)
- URL: `PUT /formularios/1`
- Body (raw JSON) (puedes mandar solo lo que cambias):
```json
{
  "edad": 29,
  "peso": 76.2
}
```

### Eliminar (DELETE)
- URL: `DELETE /formularios/1`

## 5) Correr la API

Instalar dependencias:
- `pip install -r requirements.txt`

Levantar servidor:
- `uvicorn main:app --reload`

Docs (Swagger):
- `http://127.0.0.1:8000/docs`
`http://127.0.0.1:8000/redoc`
