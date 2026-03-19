import pyodbc
from src.config import Config

class DatabaseManager:
    def __init__(self):
        self.connection_string = Config.CONNECTION_STRING
        self.conn = None

    def get_connection(self):
        if self.conn is None:
            try:
                self.conn = pyodbc.connect(self.connection_string)
            except Exception as e:
                print(f"Error connecting to database: {e}")
                raise
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def fetch_one(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            row = cursor.fetchone()
            conn.commit() # Commit after fetch to ensure transaction is saved (important for INSERT OUTPUT)
            return row
        except Exception as e:
            print(f"Query error: {e}")
            raise
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            rows = cursor.fetchall()
            conn.commit()
            return rows
        except Exception as e:
            print(f"Query error: {e}")
            raise
        finally:
            cursor.close()

    def execute_commit(self, query, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
        except Exception as e:
            print(f"Query error: {e}")
            raise
        finally:
            cursor.close()
