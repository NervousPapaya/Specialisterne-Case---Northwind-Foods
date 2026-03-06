# Case: Northwind Foods

This is a repo holding a number of scripts related to handling postgreSQL databases in python.

## Description
This is the output of the case Northwind Foods, which was the focus of week 6 of my course at Specialisterne ApS.

The project has a number of distinct components:
1. Connecting to a postgresql database "northwind"; This is handled by connection.py in the db folder
2. Visualization of data; This is handled by main.py
3. Creating, read, updating and deleting rows in a database log table ("data_notes"). This is handled by data_notes_CRUD.py

As an aside, I also made a small module to handle checking object types, called type_control.py (in error_handling). Its intended use is for the commands in the CRUD module. 

Below is an outline of the core parts
### Connection.py
This module contains a Connector class which handles all connection with the database northwind. 
As this was an exercise focusing purely on working with databases, a database password has been hardcoded in with no thought to security.
Its methods include
* connect and close; open and close the database connection
* query and query_as_df; these methods handle querying the database and returns the result as either a list of tuples or a dataframe, respectively.
* execute; handles other SQL commands sent to the database. It is used only by the CRUD class.

### data_notes_CRUD.py
This module has methods for creating, reading, updating and deleting rows in a table called data_notes. 
Its intended use is for logging comments about data in the database.
Other than the mentioned methods, there is also a method for creating the data_notes table from scratch, as well as clearing all rows in the table.

### main.py 
This script holds the main data visualizations of the project. It creates some bar plots and a scatter plot showing some parts of the data.
The script depends on the functions held in plots.py in the analysis folder.


## Getting Started
As the data this project was built on is not distributed, not all of it is directly applicable.
Specifically, the visualizations in main.py will not run without the specific database setup it was designed for. It is too hardcoded to general table names and such.

However, you can salvage something from the connection and CRUD modules. 
Essentially, you need a database first. Then, grab the src directory. If you want to test the basic functionality, grab the test directory as well.

### Dependencies
A full list of dependencies can be found in requirements.txt. At least you will need
* pandas
* psycopg2

You will also need a postgreSQL database. 

### Executing program
Once you have a database set up, do the following:
* You need to edit the connection module. It assumes a certain setup (host, database, user and password) which can be found in the init of the Connector class in connection.py. You should edit these variables to fit your setup (likely just database and password). 
* Now you can try querying your database. See some of the functions in main.py for examples of how to use the query and query_as_df methods.
* If you want to test the CRUD class, open testing_crud.py. Make sure to run the set_up_table method or set up a table of your own first.
* Make sure the table you want to use the CRUD class for is named "data_notes", or that you have edited the data_notes_CRUD.py script accordingly.
* Finally, run some of the lines in testing_crud.py, to see how to use the create, read, update and destroy methods.


## Authors

Me
