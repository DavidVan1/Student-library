from .utils.postgres_db import PostgresDB
from .utils import consts 

class InformationSystem:
    def __init__(self, db: PostgresDB):
        self.db = db
    
    def get_students(self):
        students=self.db.get_all_data(consts.STUDENT_TABLE)
        return students

    def insert_student(self, data_dict):
        student=self.db.insert_data(consts.STUDENT_TABLE, data_dict)
        return student
    
    def get_books(self):
        books=self.db.get_all_data(consts.BOOK_TABLE)
        return books

    def insert_book(self, data_dict):
        book=self.db.insert_data(consts.BOOK_TABLE, data_dict)
        return book
    
    