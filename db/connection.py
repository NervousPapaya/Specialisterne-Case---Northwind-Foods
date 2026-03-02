import psycopg2

import pandas as pd

class Connector:
    def __init__(self):
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

    def query(self,query: str):
        """This method handles querying the database."""
        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()

        return rows


    def query_as_df(self,query: str):
        """This is alternative query method. It fetches the result as a dataframe."""
        cur = self.conn.cursor()
        cur.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=columns)
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except Exception:
                pass
        return df

