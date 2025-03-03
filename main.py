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
    print("\t[8] to list unreturned books")
    print("\t[9] to exit")


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


def get_students(information_system: InformationSystem):
    students=information_system.get_students()
    for student in students:
        id, name, surname, programme = student
        print(f"{id}, {name} {surname} - {programme}")


def add_author(information_system: InformationSystem):
    print("Author details:")
    while True:
        try:
            name=input("Name: ")
            surname=input("Surname: ")
        except Exception as e:
            print(e)
            continue
        break
    information_system.insert_author({"name": name, "surname": surname})


def get_authors(information_system: InformationSystem):
    authors=information_system.get_authors()
    for author in authors:
        id, name, surname = author
        print(f"{id}, {name} {surname}")

if __name__== "__main__":
    
    while True:
        while True:
            try:
                print_menu()
                menu_choice=int(input("Menu choice: "))
                if menu_choice < 0 or menu_choice > 9:
                    raise Exception("Invalid menu choice")
                break
            except Exception as e:
                print(e)
                print("Enter a valid choice")
        
        if menu_choice == 0:
            add_student(information_system)

        if menu_choice == 1:
            add_author(information_system)
        
        if menu_choice == 5:
            get_students(information_system)
        
        if menu_choice == 9:
            break