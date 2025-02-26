import psycopg2

from psycopg2 import sql


if __name__ == "__main__":
    conn=psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="password"
    )



    conn.close()