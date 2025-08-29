import os
from typing import List

import psycopg2
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

    def fetch_all(self, *args, **kwargs):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(*args)

                if cur.description is None:
                    return None

                columns = [value.name for value in cur.description]

                query_result = [
                    dict(zip(columns, row))
                    for row in cur.fetchall()
                ]

            return query_result

    def fetch_one(self, query: str, params: tuple = ()):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchone()

    def execute_query(self, query: str, params: tuple = ()) -> List[dict]:
        with self.get_connection() as conn:
            result = self.fetch_all(query, params)
            conn.commit()
            return result
