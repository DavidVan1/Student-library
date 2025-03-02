import psycopg2
import psycopg2.extras
import traceback

from psycopg2 import sql

class PostgresDB:
    def __init__(self, host, database, user, password):
        self.connection=None
        self.host=host
        self.database=database
        self.user=user
        self.password=password
    
    def connect(self):
        try:
            self.connection=psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Connected")
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.connection = None

    def insert_data(self, table_name, data_dict):
        if self.connection is None or self.connection.closed:
            self.connect()
        
        with self.connection, self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            try:
                insert_query=sql.SQL(
                    """
                    INSERT INTO {} ({})
                    VALUES ({})
                    RETURNING *;
                    """
                ).format(
                    sql.Identifier(table_name),
                    sql.SQL(',').join(map(sql.Identifier, data_dict.keys())),
                    sql.SQL(',').join(map(sql.Literal, data_dict.values()))
                )
                cur.execute(insert_query)
                insert = cur.fetchone()
            except Exception as e:
                traceback.print_exc()
                print(f"Error {e}")

        self.connection.close()
        return insert
    

    def get_all_data(self, table_name):
        result = []
        if self.connection is None or self.connection.closed:
            self.connect()
        
        with self.connection, self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            try:
                select_query=sql.SQL(
                    """
                    SELECT *
                    FROM {}
                    """
                ).format(
                    sql.Identifier(table_name)
                )
                cur.execute(select_query)
                result = cur.fetchall()
            except Exception as e:
                traceback.print_exc()
                print(f"Error {e}")
        
        self.connection.close()
        return result
        
    

    def get_data_simple_condition(self, table_name, columns=[], condition_column=None, condition_value=None):
        result = []

        if self.connection is None or self.connection.closed:
            self.connect()
        
        with self.connection, self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            try:
                if condition_column is None:
                    select_query=sql.SQL(
                        """
                        SELECT {}
                        FROM {}
                        """
                    ).format(
                        sql.SQL(',').join(map(sql.Identifier, columns)),
                        sql.Identifier(table_name)
                    )
                else:
                    select_query=sql.SQL(
                        """
                        SELECT {}
                        FROM {}
                        WHERE {} = {}
                        """
                    ).format(
                        sql.SQL(',').join(map(sql.Identifier, columns)),
                        sql.Identifier(table_name),
                        sql.Identifier(condition_column),
                        sql.Literal(condition_value)
                    )
                cur.execute(select_query)
                result=cur.fetchall()
            except Exception as e:
                traceback.print_exc()
                print(f"Error {e}")
        self.connection.close()
        return result
    

    def get_join_results(self, table_name_a, table_name_b, join_coulmn_name_a, join_coulmn_name_b=None):
        result=[]
        join_coulmn_name_b = join_coulmn_name_b or join_coulmn_name_a
        if self.connection == None or self.connection.closed:
            self.connect()
        
        with self.connection, self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            try:
                join_query=sql.SQL(
                    """
                    SELECT *
                    FROM {}
                    JOIN {} ON {}.{} = {}.{}
                    """
                ).format(
                    sql.Identifier(table_name_a),
                    sql.Identifier(table_name_b),
                    sql.Identifier(table_name_a),
                    sql.Identifier(join_coulmn_name_a),
                    sql.Identifier(table_name_b),
                    sql.Identifier(join_coulmn_name_b),
                )
                cur.execute(join_query)
                result=cur.fetchall()
            except Exception as e:
                traceback.print_exc()
                print(f"Error {e}")
        self.connection.close()
        return result
    

    def update_table(self, table_name, updates, conditions):

        if self.connection == None or self.connection.closed:
            self.connect()

        with self.connection, self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            try:
                set_clause = sql.SQL(", ").join(
                    sql.Composed([sql.Identifier(k), sql.SQL(" = "), sql.Placeholder(k)]) for k in updates.keys()
                )
                
                where_clause = sql.SQL(" AND ").join(
                    sql.Composed([sql.Identifier(k), sql.SQL(" = "), sql.Placeholder(k)]) for k in conditions.keys()
                )

                update_query = sql.SQL(
                    """
                    UPDATE {} 
                    SET {} 
                    WHERE {}
                    """
                    ).format(
                    sql.Identifier(table_name),
                    set_clause,
                    where_clause
                )

                values = {**updates, **conditions}

                cur.execute(update_query, values)
                print(f"Updated {cur.rowcount} rows in {table_name}")

            except Exception as e:
                traceback.print_exc()
                print(f"Error: {e}")
        self.connection.close()