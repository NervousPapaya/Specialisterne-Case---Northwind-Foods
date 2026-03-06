from db.connection import Connector
import matplotlib.pyplot as plt


db = Connector()
db.connect()

def bar_plot(query: str,rot: int=None, title: str = None):
    """this function creates a bar plot from a query. It assumes that the first column is to be used as the x-vales"""
    if query is None:
        raise ValueError("You must supply a query.")
    rows = db.query_as_df(query)
    bar_plot_df(rows,rot,title)

def plot_query(query, rot: int = None,title: str = None):
    """this function creates a plots from a data frame. It assumes that the first column is to be used as the x-vales"""
    if query is None:
        raise ValueError("You must supply a query.")
    df = db.query_as_df(query)
    plot_df(df,rot,title)


def bar_plot_df(df,rot:int=None, title: str = None):
    """this function creates a bar plot from a data frame. It assumes that the first column is to be used as the x-vales"""
    df.set_index(df.columns[0], inplace=True)
    df.plot(kind="bar" ,figsize=(14 ,7))
    if title is not None:
        plt.title(title)
    if rot is not None:
        plt.xticks(rotation=rot)
    plt.tight_layout()
    plt.show()

def plot_df(df,rot:int=None, title: str = None):
    """this function creates a plots from a data frame. It assumes that the first column is to be used as the x-vales"""
    df.set_index(df.columns[0], inplace=True)
    df.plot(figsize=(14 ,7))
    if title is not None:
        plt.title(title)
    if rot is not None:
        plt.xticks(rotation=rot)
    plt.tight_layout()
    plt.show()



def scatter_plot(x_values, y_values, x_label, y_label, title: str = None):
    plt.figure(figsize=(14, 7))
    plt.scatter(x_values, y_values, alpha=0.6)
    if x_label is not None:
        plt.xlabel(x_label)
    if y_label is not None:
        plt.ylabel(y_label)
    if title is not None:
        plt.title(title)
    plt.show()