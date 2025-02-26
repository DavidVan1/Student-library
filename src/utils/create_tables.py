import psycopg2

from psycopg2 import sql


if __name__ == "__main__":
    conn=psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="password"
    )


    with conn, conn.cursor() as cur:
        create_student_table_query=sql.SQL(
            """
            DROP TABLE IF EXISTS student;
            CREATE TABLE student (
                student_id SERIAL PRIMARY KEY,
                name VARCHAR(128),
                surname VARCHAR(128),
                grade INT
            );
            """
        )
        cur.execute(create_student_table_query)

    conn.close()