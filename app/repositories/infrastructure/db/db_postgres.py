import os

import psycopg2
import psycopg2.extras
from contextlib import contextmanager

from app.repositories.infrastructure.db.database import Database


DATABASE_CONFIG = {
    "dbname": os.getenv('DB_NAME', 'events_db'),
    "user": os.getenv('DB_USER', 'user'),
    "password": os.getenv('DB_PASSWORD', 'mysecretpassword'),
    "host": os.getenv('DB_HOST', 'localhost'),
    "port": os.getenv('DB_PORT', '5432')
}


class PostgresDB(Database):
    def __init__(self, config: dict=None):
        if config is None:
            config = DATABASE_CONFIG
        self.config = config

    @contextmanager
    def get_connection(self):
        conn = psycopg2.connect(**self.config)
        try:
            yield conn
        finally:
            conn.close()

    def fetch_all(self, query: str, params: tuple = ()):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(query, params)
                return cur.fetchall()

    def fetch_one(self, query: str, params: tuple = ()):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(query, params)
                return cur.fetchone()

    def execute_query(self, query: str, params: tuple = ()):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                return cur.rowcount
