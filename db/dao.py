import psycopg2
from psycopg2.extensions import parse_dsn
import socket
import os



class PostgresDAO:
    def __init__(self, host, port, database, user, password):
        self.host=host
        self.port=port
        self.database=database
        self.user=user
        self.password=password
        self.sslmode="require"        
        self.conn=None
        self.option=os.getenv("ENDPOINT") or None
        self.conn= self._create_conn()
        self.cursor=self.conn.cursor()
        
    def _create_conn(self):
        if os.getenv('HOST') != 'localhost':
            conn = psycopg2.connect(
                        host=self.host,
                        database=self.database,
                        user=self.user,
                        password=self.password,
                        sslmode="require",
                        options=self.option
                    )
        else:
            conn = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    sslmode=None
                )
        return conn
        
    def execute_query(self, query, params=None):
        """Check for an existing connection and cursor.
        If the connection is closed, create a new connection and cursor.
        Use the cursor to execute the query and params.
        Close the cursor and connection afterward."""
    
        try:
            if not self.conn or self.conn.closed:
                self.conn = self._create_conn()
                self.cursor = self.conn.cursor()
            self.cursor.execute(query, params)
            self.conn.commit()
            
            #FOR insertion dont return anything for FETCH return result
            try: 
                results = self.cursor.fetchall()
                return results
            except psycopg2.ProgrammingError as e:
                print ("No rows to return")
            

        except psycopg2.Error as e:
            print(f"Error executing query: {e}")

        finally:
            if self.conn:
                self.close_connection()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
