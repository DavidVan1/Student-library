from .src.utils.postgres_db import PostgresDB
from .src.InformationSystem import InformationSystem

pg_db=PostgresDB(
    host="localhost",
        database="postgres",
        user="postgres",
        password="password"
)

information_system=InformationSystem(db=pg_db)




