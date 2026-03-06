import psycopg2

import pandas as pd

class Connector:
    """This class handles the connection to the database northwind."""
    def __init__(self):
        #NOTE: As this is an exercise, the server password has been hardcoded in.
        self.host = "localhost"
        self.database = "northwind"
        self.user = "postgres"
        self.password = "Hestehop11235!"
        self.conn = None

    def connect(self):
        """This method handles opening the connection to the database"""
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(host = self.host, dbname=self.database, user=self.user, password=self.password)
                print(f"Connection established to database {self.database}")
            except Exception as e:
                print(f"Connection not established due to", e)

    def close(self):
        """This method handles closing the connection to the database"""
        if self.conn:
            self.conn.close()
            self.conn = None
            print(f"Closed connection to database {self.database}")

    def query(self, query: str,parameters = None):
        """This method handles querying the database. It fetches the result as a list of tuples."""
        if self.conn is None:
            raise RuntimeError("Database connection must be established before running a query. Call connect() first")
        cur = self.conn.cursor()
        cur.execute(query,parameters)
        rows = cur.fetchall()

        return rows


    def query_as_df(self,query: str, parameters = None):
        """This is alternative query method. It fetches the result as a dataframe."""
        if self.conn is None:
            raise RuntimeError("Database connection must be established before running a query. Call connect() first")
        cur = self.conn.cursor()
        cur.execute(query, parameters)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=columns)
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except Exception:
                pass
        return df

    def execute(self, statement: str,parameters = None, *, commit: bool = False, close: bool = True):
        """This method is to handle more general executions sent to the database.
        The parameters can be either a list or a dictionary.
        The commit argument decides whether a change is commited to the database automatically. It is False by default.
        As the use case is different from that of the query method, this method does not assume the connection is open.
        It opens the connection if need be and has an argument which determines whether to close the connection.
         By default, the connection is closed at the end."""
        if not self.conn:
            self.connect()
        cur = self.conn.cursor()
        cur.execute(statement, parameters)
        if commit is True:
            self.conn.commit()
        if close is True:
            self.close()