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
                name VARCHAR(128) NOT NULL,
                surname VARCHAR(128) NOT NULL,
                grade INT
            );
            """
        )
        cur.execute(create_student_table_query)
    
        create_book_table_query=sql.SQL(
            """
            DROP TABLE IF EXISTS book;
            CREATE TABLE book (
                book_id SERIAL PRIMARY KEY,
                title VARCHAR(128),
                author_id INT,
                copies_available INT DEFAULT 1
            );
            """
        )
        cur.execute(create_book_table_query)


    conn.close()