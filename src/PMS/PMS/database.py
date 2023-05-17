import sqlite3
import pyodbc
from sqlite3 import Error

class database:

    def execute_sql(self, sql):
        self.conn = self.create_connection()
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        self.conn.commit()

    def select_sql(self, sql):
        self.conn = self.create_connection()
        self.cur = self.conn.cursor()
        self.cur.execute(sql)
        return self.cur.fetchall()


    def create_sqlite_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(db_file)

            return conn
        except Error as e:
            print(e)

        return None


    def create_connection(self):
        try:
            conn = pyodbc.connect("DRIVER={{SQL Server}};SERVER={server}; database={database}; \
                   trusted_connection=no;UID={uid};PWD={pwd}".format(server="10.96.101.4", database="NaNa", uid="sa", pwd="134"))

            return conn
        except Error as e:
            print(e)

        return None
