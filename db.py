import os
from contextlib import contextmanager

import psycopg2


def _conn_params() -> dict:
    """
    Forma sencilla (para aprender):
    - Host: localhost
    - Puerto: 5432
    - Usuario: postgres
    - Password: postgres (cámbialo al tuyo)
    - Base: mi_form_db

    Puedes cambiarlo con variables de entorno:
    PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE
    """
    return {
        "host": os.getenv("PGHOST", "localhost"),
        "port": int(os.getenv("PGPORT", "5432")),
        "user": os.getenv("PGUSER", "postgres"),
        "password": os.getenv("PGPASSWORD", "postgres"),
        "dbname": os.getenv("PGDATABASE", "mi_form_db"),
    }


@contextmanager
def get_conn():
    conn = psycopg2.connect(**_conn_params())
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
