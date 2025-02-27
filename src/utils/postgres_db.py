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
    
    def connect(self):
        if self.connection is None:
            try:
                self.connection=psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                print("Connected")
            except Exception as e:
                print(f"Error connecting to database: {e}")
                self.connection = None