import psycopg2

conn=psycopg2.connect(
    host="localhost",
    databese="postgres",
    user="postgres",
    password="password"
)

conn.close()