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


def is_book_available(information_system: InformationSystem, book_id):
    return information_system.get_available_copies(book_id) > 0


def student_exists(information_system: InformationSystem, student_id):
    return information_system.get_student_by_id(student_id) != []


def borrow_book(information_system: InformationSystem):
    while True:
        try:
            student_id=input("Student id: ")

            if not student_exists(information_system, student_id):
                print(f"No student with ID {student_id}")
                return
            
            book_id=input("Book id: ")
        except Exception as e:
            print(e)
            continue
        break
    if not is_book_available(information_system, book_id):
        print("Book unavailable")
        return

    information_system.borrow_book({"student_id": student_id, "book_id": book_id})
    print("Book borrowed")


def print_loans_of_student(information_system: InformationSystem, loans):
    print("\n*******************************************")
    for loan in loans:
        borrow_id, book_id, borrow_date = loan
        title=information_system.get_book_title_by_id(book_id)
        print(f"Borrow ID: {borrow_id}")
        print(f"\t Title: {title}")
        print(f"\t Borrowed on: {borrow_date}\n")

def get_loans_set(loans):
    loans_set=set()

    for loan in loans:
        loans_set.add(loan[0])

    return loans_set

def return_book(information_system: InformationSystem):
    while True:
        try:
            student_id=int(input("Student id: "))
        except Exception as e:
            print(e)
            continue
        break

    loans = information_system.get_loans_by_student(student_id)
    if not loans:
        print("Student has no borrowed books.")
        return
    print_loans_of_student(information_system, loans)
    loans_set = get_loans_set(loans)

    selected_borrows=[]
    print("Choose book to return (press -1 to finish adding): ")
    while True:
        try:
            borrow_id = int(input("Borrow ID: "))

            if borrow_id == -1:
                break
            if borrow_id not in loans_set:
                print("Please choose ids from above")
                continue
            
            selected_borrows.append(borrow_id)
            loans_set.remove(borrow_id)
        except:
            print(e)
            continue
        if loans_set: continue
        break
    
    for borrow in selected_borrows:
        information_system.return_book(borrow)


def print_unreturned_books(information_system: InformationSystem,borrow_records):

    for record in borrow_records.keys():
        name, surname, programme = information_system.get_student_by_id(record)[0]
        print("\n*******************************************")
        print(f"Student: {name} {surname}")

        for borrow in borrow_records[record]:
            title=information_system.get_book_title_by_id(borrow["book_id"])
            borrow_date = borrow["borrow_date"]
            id=borrow["borrow_id"]
            print("\nBook:", end='')
            print(f"\t Title: {title}")
            print(f"\t Borrowed on: {borrow_date}")
            print(f"\t Borrow ID: {id}")


def get_unreturned_books(information_system: InformationSystem):
    borrows=information_system.get_unreturned_books()
    
    borrow_records = {}

    for borrow in borrows:
        student_id, borrow_id, book_id, borrow_date = borrow
        if student_id not in borrow_records:
            borrow_records[student_id] = []
    
        borrow_records[student_id].append({
            "borrow_id": borrow_id,
            "book_id": book_id,
            "borrow_date": borrow_date
        })
    
    print_unreturned_books(information_system, borrow_records)



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
        
        elif menu_choice == 3:
            borrow_book(information_system)
        
        elif menu_choice == 4:
            return_book(information_system)
        
        elif menu_choice == 5:
            get_students(information_system)
        
        elif menu_choice == 6:
            get_books(information_system)

        elif menu_choice == 7:
            get_authors(information_system)
        
        elif menu_choice == 8:
            get_unreturned_books(information_system)
        
        elif menu_choice == 9:
            break