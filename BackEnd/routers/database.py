import psycopg2
from contextlib import contextmanager

DATABASE_URL = "postgres://tsdbadmin:tmt2jvnfymsm3wv8@o8dbraumqo.fpukhdb1kr.tsdb.cloud.timescale.com:36895/tsdb?sslmode=require"

@contextmanager
def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()
