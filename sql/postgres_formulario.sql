-- Script para PostgreSQL (ejecútalo con psql)
-- 1) Crea la base de datos
-- 2) Crea la tabla "formularios"
-- 3) Agrega datos de ejemplo (INSERT)
-- 4) Te deja ejemplos de SELECT/UPDATE/DELETE
--
-- Tipos de datos (muy resumido):
-- - VARCHAR(n): texto variable hasta n caracteres (más flexible para nombres, emails).
-- - CHAR(n): texto de longitud fija n (útil para códigos fijos, ej: 'M'/'F' con CHAR(1)).
-- - INT: números enteros (edad, cantidad).
-- - FLOAT: números con decimales (peso, altura). En finanzas suele preferirse NUMERIC.

CREATE DATABASE mi_form_db;

-- En psql puedes conectarte así:
-- \c mi_form_db

CREATE TABLE formularios (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE,
  edad INT,
  peso FLOAT,
  genero CHAR(1),
  creado_en TIMESTAMP NOT NULL DEFAULT NOW()
);

-- -------------------------
-- DATOS DE EJEMPLO (INSERT)
-- -------------------------
INSERT INTO formularios (nombre, apellido, email, edad, peso, genero)
VALUES
  ('Juan', 'Pérez', 'juan@mail.com', 25, 70.5, 'M'),
  ('Ana', 'Gómez', 'ana@mail.com', 30, 60.2, 'F'),
  ('Andrés', 'López', 'andres@mail.com', 22, 68.0, 'M')
ON CONFLICT (email) DO NOTHING;

-- -------------------------
-- CONSULTAR (SELECT)
-- -------------------------
-- SELECT * FROM formularios;
-- SELECT * FROM formularios WHERE id = 1;

-- -------------------------
-- EDITAR (UPDATE)
-- -------------------------
-- UPDATE formularios SET edad = 26 WHERE id = 1;
-- UPDATE formularios SET peso = 71.3, genero = 'M' WHERE id = 1;

-- -------------------------
-- ELIMINAR (DELETE)
-- -------------------------
-- DELETE FROM formularios WHERE id = 1;
