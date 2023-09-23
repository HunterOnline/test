import sqlite3

import logging


class UserDatabase:
    def __init__(self, path_to_db="data/user_db.db"):
        self.path_to_db = path_to_db
        self.buf_user_data = None
    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logging)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_user_table(self):  # CREATE  TABLE user( id INTEGER PRIMARY KEY)
        sql = """
              CREATE TABLE UserTable(
                  id INTEGER PRIMARY KEY,
                  id_user int NOT NULL,
                  user_name varchar(255) NOT NULL
                  );
      """
        self.execute(sql, commit=True)

    def add_user(self, id_user: int, user_name: str):
        sql = """
               INSERT INTO UserTable(id_user, user_name) VALUES(?,?)
               """
        parameters = (id_user, user_name)
        self.execute(sql, parameters=parameters, commit=True)

    def count_user(self):
        return self.execute("SELECT COUNT(*) FROM UserTable;", fetchall=True)

    def select_all_sets(self):
        sql = """
        SELECT * FROM UserTable
        """
        return self.execute(sql, fetchall=True)

    def select_user_id(self):
        sql = """
        SELECT id_user FROM UserTable
        """
        return self.execute(sql, fetchall=True)

    def select_user_parm(self, id_user: int):

        return self.execute("""SELECT * FROM UserTable WHERE id=?""", (id_user, ), fetchall=True)

    def delete_user(self, id_user: int):
        self.execute("""DELETE FROM UserTable WHERE id=?""", (id_user,), commit=True)

    def delete_all(self,):
        self.execute("""DELETE FROM UserTable """, commit=True)

    def unload_user_data(self):
        lst_id = [i[0] for i in self.select_user_id()]
        logging.info('МeDbot unload_USER_data -> successfully')
        self.buf_user_data = lst_id



def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
