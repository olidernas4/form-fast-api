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

> En Postman, selecciona el método HTTP, pon la URL, elige `Body` > `raw` > `JSON` y agrega el JSON de ejemplo.

### Crear (POST)
- URL: `POST /formularios`
- Headers:
  - `Content-Type: application/json`
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

### Ejemplo de JSON mínimo válido para crear
```json
{
  "nombre": "Ana",
  "apellido": "Gómez",
  "genero": "F"
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
- Headers:
  - `Content-Type: application/json`
- Body (raw JSON):
```json
{
  "edad": 29,
  "peso": 76.2
}
```

### Ejemplo de JSON completo para editar
```json
{
  "nombre": "Carlos",
  "apellido": "Ruiz",
  "email": "carlos.nuevo@mail.com",
  "edad": 29,
  "peso": 76.2,
  "genero": "M"
}
```

### Notas importantes
- Para `genero`, usa solo un carácter: `"M"` o `"F"`.
- Si envías un `PUT` con un JSON vacío, la API responde:
  - `{"mensaje": "Nada para actualizar"}`
- El campo `email` es opcional y, si lo envías, debe tener formato válido.

### Eliminar (DELETE)
- URL: `DELETE /formularios/1`

## 5) Correr la API

Instalar dependencias:
- `pip install -r requirements.txt`

Levantar servidor:
- `uvicorn main:app --reload`

Docs (Swagger):
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## 6) Git

Esta sección explica cómo colaborar con un compañero usando Git y ramas, para evitar conflictos de código.

### 6.1) Recomendación general

- Cada persona debe trabajar en su propia rama, no directamente en `main`.
- Usen nombres claros para las ramas: por ejemplo `feature/crear-formulario`, `feature/editar-formulario`, `fix/email-validacion`.
- Antes de empezar a trabajar, siempre actualiza la rama `main` del repositorio remoto.

### 6.2) Paso a paso para trabajar sin conflictos

1. Clona el repositorio una sola vez:
   - `git clone <URL-del-repositorio>`
2. Entra a la carpeta del proyecto:
   - `cd mi_proyecto_fastapi`
3. Actualiza `main` antes de crear tu rama:
   - `git checkout main`
   - `git pull origin main`
4. Crea una rama nueva para tu cambio:
   - `git checkout -b feature/nombre-de-tu-cambio`
5. Trabaja en tu rama y haz cambios en el código.
6. Guarda tus cambios con commits pequeños y claros:
   - `git add .`
   - `git commit -m "Agregar ejemplo JSON de Postman"`
7. Antes de subir tu rama, actualiza `main` y rebase o merge:
   - `git checkout main`
   - `git pull origin main`
   - `git checkout feature/nombre-de-tu-cambio`
   - `git rebase main`  (o `git merge main` si prefieres)

### 6.3) Subir tu rama y crear un Pull Request

1. Sube tu rama al remoto:
   - `git push origin feature/nombre-de-tu-cambio`
2. En la plataforma de Git (GitHub/GitLab/Bitbucket):
   - Crea un Pull Request (PR) o Merge Request (MR) desde tu rama hacia `main`.
   - Describe qué cambiaste y por qué.
3. Tu compañero revisa el PR y aprueba los cambios.
4. Una vez aprobado, se puede fusionar a `main`.

### 6.4) Cómo evitar conflictos al hacer `pull` o `merge`

- Siempre actualiza `main` con `git pull origin main` antes de empezar una nueva rama.
- Evita editar exactamente las mismas líneas que tu compañero.
- Si hay conflictos, Git mostrará los archivos con conflictos.
  - Abre el archivo y busca las marcas `<<<<<<<`, `=======`, `>>>>>>>`.
  - Decide cuál cambio conservar o combina ambos cambios.
  - Luego haz:
    - `git add <archivo-con-conflicto>`
    - `git rebase --continue`  (si usaste rebase)
    - o `git commit`  (si usaste merge)
- Finalmente, sube los cambios corregidos:
  - `git push origin feature/nombre-de-tu-cambio`

### 6.5) Ejemplo rápido de flujo colaborativo

1. Yo actualizo `main`:
   - `git checkout main`
   - `git pull origin main`
2. Creo mi rama:
   - `git checkout -b feature/agregar-guia-git`
3. Hago mis cambios y commit:
   - `git add GUIA.md`
   - `git commit -m "Agregar sección Git a la guía"`
4. Actualizo `main` otra vez antes de enviar:
   - `git checkout main`
   - `git pull origin main`
   - `git checkout feature/agregar-guia-git`
   - `git rebase main`
5. Subo la rama y creo el Pull Request.

Con este flujo, cada uno trabaja en su propia rama y se reduce mucho el riesgo de conflictos.
