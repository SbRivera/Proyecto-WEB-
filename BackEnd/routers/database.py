import psycopg2
from contextlib import contextmanager

DATABASE_URL = "postgresql://postgres:taco@localhost/proyecto"

@contextmanager
def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()
