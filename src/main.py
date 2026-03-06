from db.connection import Connector
from analysis.plots import bar_plot, bar_plot_df, plot_df, scatter_plot

#This script handles the visualizations in the exercise

def get_sales_per_country(db):
    """This function produces the dataframe with sales per country"""
    query = """
        SELECT shipcountry, SUM(unitprice*quantity) as "total_sales" 
        FROM orderdetails od
        LEFT JOIN orders o
        on od.orderid = o.orderid
        GROUP BY shipcountry
        ORDER BY shipcountry
    """
    return db.query_as_df(query)


def get_sales_per_product(db,limit = None):
    """This function returns a dataframe with the sales of each product.
    It can be limited to return only the top N products by total sales.
    If no limit is given, all are taken."""
    parameters = {}
    query = """
        WITH top_products AS(
        SELECT productname, SUM(od.unitprice*od.quantity) as "total_sales"
        FROM orderdetails od
        LEFT JOIN products p
        on od.productid = p.productid
        GROUP BY productname
        ORDER BY total_sales DESC)
        SELECT *
        FROM top_products
        ORDER BY productname
        """
    if limit is not None:
        query += " LIMIT %(limit)s"
        parameters["limit"] = limit
    return db.query_as_df(query, parameters)


def get_monthly_sales(db, year=1997):
    parameters ={"year": year}
    query = f"""
        SELECT EXTRACT(MONTH from orderdate) as "month", SUM(od.unitprice*od.quantity) as "total_sales"
        FROM orders o
        LEFT JOIN orderdetails od
        on o.orderid = od.orderid
        WHERE orderdate BETWEEN DATE '%(year)s-01-01' AND DATE '%(year)s-12-31'
        GROUP BY month
        ORDER BY month
    """
    return db.query_as_df(query, parameters)


def get_late_shippings():
    query = """SELECT companyname, COUNT(orderid) as "total_late"
FROM shippers s
LEFT JOIN orders o
ON  s.shipperid = o.shipvia
WHERE shippeddate > requireddate
GROUP BY companyname"""
    return query


def get_quantity_vs_unit_price(db):
    query = """
        WITH top_products AS(
        SELECT productname, COUNT(*) as quantity_sold, SUM(od.unitprice*od.quantity) as "total_sales", p.unitprice
        FROM orderdetails od
        LEFT JOIN products p
        on od.productid = p.productid
        GROUP BY productname, p.unitprice
        ORDER BY total_sales DESC)
        SELECT *
        FROM top_products
        ORDER BY productname
    """
    return db.query_as_df(query)

def main():
    db = Connector()
    db.connect()

    sales_per_country_df = get_sales_per_country(db)
    #print(sales_per_country_df)
    bar_plot_df(sales_per_country_df)

    sales_per_product_df = get_sales_per_product(db)
    #print(sales_per_product_df)
    bar_plot_df(sales_per_product_df)

    top_twenty_sales_per_prdct_df = get_sales_per_product(db,20)
    bar_plot_df(top_twenty_sales_per_prdct_df)

    bar_plot(get_late_shippings(),45, "Total late shippings by shipper")

    qty_vs_price_df = get_quantity_vs_unit_price(db)
    scatter_plot(qty_vs_price_df["quantity_sold"], qty_vs_price_df["unitprice"], "quantity",
                 "unit price", "Products quantity sold vs unit price")

    # Finally we close the database
    db.close()


if __name__ == "__main__":
    main()