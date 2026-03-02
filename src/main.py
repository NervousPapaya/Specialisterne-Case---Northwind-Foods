from db.connection import Connector
import pandas as pd
import matplotlib.pyplot as plt


def main():
    db = Connector()
    db.connect()


    rows = db.query_as_df("""SELECT shipcountry, SUM(unitprice*quantity) as "total sales" 
                      FROM Orderdetails
                      LEFT JOIN ORDERS
                        on ORDERDETAILs.orderid = ORDERS.orderid
                      GROUP BY SHIPCOUNTRY
                        ORDER BY SHIPCOUNTRY""")
    rows.set_index("shipcountry", inplace=True)
    rows.plot(kind="bar",figsize=(14,7))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print(rows)

    db.close()


if __name__ == "__main__":
    main()