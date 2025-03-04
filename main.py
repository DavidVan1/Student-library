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
    print("\t[7] to list authors")
    print("\t[8] to list loans")
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


def add_author(information_system: InformationSystem, name=None, surname=None):
    if name is None or surname is None:
        print("Author details:")
        while True:
            try:
                name=input("Name: ")
                surname=input("Surname: ")
            except Exception as e:
                print(e)
                continue
            break
    return information_system.insert_author({"name": name, "surname": surname})


def get_authors(information_system: InformationSystem):
    authors=information_system.get_authors()
    for author in authors:
        id, name, surname = author
        print(f"{id}, {name} {surname}")



def get_author_id(information_system: InformationSystem, name, surname):
    id=information_system.get_author_by_name({"name": name, "surname": surname})
    return id[0][0] if id else add_author(information_system, name, surname)[0]


def get_author_name(information_system: InformationSystem, author_id):
    return information_system.get_author_by_id(author_id)


def add_book(information_system: InformationSystem):
    print("Book details:")
    while True:
        try:
            title=input("Title: ")
            author_name=input("Author name: ")
            author_surname=input("Author surname: ")
            copies_available=int(input("Copies available: "))
        except Exception as e:
            print(e)
            continue
        break

    author_id = get_author_id(information_system, author_name, author_surname)
    information_system.insert_book({"title": title, "author_id": author_id, "copies_available": copies_available})


def get_books(information_system: InformationSystem):
    books=information_system.get_books()
    
    for book in books:
        id, title, author_id, copies_available = book
        author_name, author_surname = get_author_name(information_system, author_id)
        print("\n*******************************************")
        print(title)
        print(f"\t ID: {id}")
        print(f"\t Name: {author_name} {author_surname}")
        print(f"\t Available copies: {copies_available}")

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

        elif menu_choice == 1:
            add_author(information_system)

        elif menu_choice == 2:
            add_book(information_system)
        
        elif menu_choice == 5:
            get_students(information_system)
        
        elif menu_choice == 6:
            get_books(information_system)

        elif menu_choice == 7:
            get_authors(information_system)
        
        elif menu_choice == 9:
            break