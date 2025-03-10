from .utils.postgres_db import PostgresDB
from .utils import consts 

import datetime

class InformationSystem:
    def __init__(self, db: PostgresDB):
        self.db = db
    
    def get_students(self):
        students=self.db.get_all_data(consts.STUDENT_TABLE)
        return students

    def insert_student(self, data_dict):
        student=self.db.insert_data(consts.STUDENT_TABLE, data_dict)
        return student
    
    def get_student_by_id(self, student_id):
        student=self.db.get_data_simple_condition(consts.STUDENT_TABLE, ["name", "surname", "programme"], "student_id", student_id)
        return student
    
    def get_books(self):
        books=self.db.get_all_data(consts.BOOK_TABLE)
        return books
    
    def get_books_by_author(self, author_id):
        books=self.db.get_join_results(consts.BOOK_TABLE, consts.AUTHOR_TABLE, author_id, author_id)
        return books
    
    def get_book_title_by_id(self, book_id):
        book=self.db.get_data_simple_condition(consts.BOOK_TABLE, ["title"], "book_id", book_id)
        return book[0][0] if book else None

    def insert_book(self, data_dict):
        book=self.db.insert_data(consts.BOOK_TABLE, data_dict)
        return book
    
    def get_authors(self):
        authors=self.db.get_all_data(consts.AUTHOR_TABLE)
        return authors
    
    def insert_author(self, data_dict):
        author=self.db.insert_data(consts.AUTHOR_TABLE, data_dict)
        return author
    
    def get_author_by_name(self, conditions):
        author=self.db.get_data_multiple_conditions(consts.AUTHOR_TABLE, [], conditions)
        return author
    
    def get_author_by_id(self, author_id):
        name, surname=self.db.get_data_simple_condition(consts.AUTHOR_TABLE, ["name", "surname"], "author_id", author_id)[0]
        return name, surname
    
    def get_available_copies(self, book_id):
        available_copies=self.db.get_data_simple_condition(consts.BOOK_TABLE, ["copies_available"], "book_id", book_id)
        return available_copies[0][0] if available_copies else -1
    
    def get_loans(self, student_id):
        loans=self.db.get_data_simple_condition(consts.BORROW_TABLE, ["borrow_id", "book_id", "borrow_date", "return_date"], 
                                                "student_id", student_id)
        return loans
    
    def get_loans_by_student(self, student_id):
        loans=self.db.get_data_multiple_conditions(consts.BORROW_TABLE, ["borrow_id", "book_id", "borrow_date"], 
                                                   {"student_id": student_id, "returned": "FALSE"})
        return loans
    
    def get_unreturned_books(self):
        books=self.db.get_data_multiple_conditions(consts.BORROW_TABLE, ["student_id", "borrow_id","book_id", "borrow_date"],
                                                   {"returned": "FALSE"})
        return books
    
    def borrow_book(self, data_dict):
        borrow=self.db.insert_data(consts.BORROW_TABLE, data_dict)
        copies = self.get_available_copies(data_dict["book_id"])
        self.db.update_table(consts.BOOK_TABLE, {"copies_available": copies-1}, {"book_id": data_dict["book_id"]})
        return borrow
    
    def return_book(self, borrow_id):
        book_id=self.db.get_data_simple_condition(consts.BORROW_TABLE, ["book_id"], "borrow_id", borrow_id)[0][0]
        self.db.update_table(consts.BORROW_TABLE, {"returned": "TRUE", "return_date": datetime.date.today()}, 
                             {"borrow_id": borrow_id})
        self.db.update_table(consts.BOOK_TABLE, {"copies_available": self.get_available_copies(book_id)+1}, 
                             {"book_id": book_id})
    

    