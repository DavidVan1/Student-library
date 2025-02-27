import psycopg2
import psycopg2.extras
import traceback

from psycopg2 import sql

class PostgresDB:
    def __init__(self, host, database, user, password):
        self.connection=None
        self.host=host
        self.database=database
        self.user=user
        self.password=password