from db.connection import Connector

def main():
    db = Connector()

    db.connect()

    print("Testing query method")
    rows = db.query("SELECT * FROM products LIMIT 5")
    for row in rows:
        if row is None:
            break
        print(row)


    print("Testing query_as_df")
    df  = db.query_as_df("SELECT * FROM products LIMIT 5")
    print(df)
    db.close()

if __name__ == "__main__":
    main()