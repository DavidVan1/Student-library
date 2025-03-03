from src.utils.postgres_db import PostgresDB
from src.InformationSystem import InformationSystem

pg_db=PostgresDB(
    host="localhost",
        database="postgres",
        user="postgres",
        password="password"
)

information_system=InformationSystem(db=pg_db)


def print_menu():
    print("\n*******************************************")
    print("Menu options:")
    print("\t[0] to add a student")
    print("\t[1] to add a author")
    print("\t[2] to add a book")
    print("\t[3] to borrow a book")
    print("\t[4] to return a book")
    print("\t[5] to list students")
    print("\t[6] to list books")
    print("\t[7] to list loans")


def add_student(information_system: InformationSystem):
    print("Student details:")
    while True:
        try:
            name=input("Name: ")
            surname=input("Surname: ")
            programme=input("Programme: ")
        except Exception as e:
            print(e)
            continue
        break
    information_system.insert_student({"name": name, "surname": surname, "programme": programme})


if __name__== "__main__":
    add_student(information_system)