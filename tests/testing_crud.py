from db.data_notes_CRUD import CRUD


# This script is for testing the methods in the CRUD class.
# Just out comment the line with the CRUD method you want to test

CRUD = CRUD()

#This method can be used to create the table if it does not already exist in the database
#CRUD.set_up_table()

# Testing if we can create a single row
CRUD.create(10297,"order","This order consists of only two types of products")

#Testing if the basic read method reads the whole table
#CRUD.read()

# Testing if we can create multiple rows
#CRUD.create(10298,"order","This order consists of only three types of products", commit = False, close = False)
#CRUD.create(4,"employee", "This employee is the oldest in the company", commit = False, close = False)
#CRUD.create(9,"employee", "This employee is the second youngest in the company", commit = True, close = True)
#CRUD.read()



#Testing if we can read specific rows
#CRUD.read(data_notes_id=3)
#Testing if we can read specific entity ids
#CRUD.read(entity_id=10297)

#Testing if we can read specific types
#CRUD.read(entity_type="employee")


#CRUD.update(data_notes_id=4,comment="This employee is the youngest in the company")
#CRUD.read(data_notes_id=4)

#Testing if we can delete a specific row
#CRUD.delete(4)
#CRUD.read()



#Testing if we can delete everything
#CRUD.delete_all_rows()

#if __name__ == "__main__":
