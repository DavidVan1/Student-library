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
    