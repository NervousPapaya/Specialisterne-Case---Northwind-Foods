from db.connection import Connector
from error_handling.type_control import test_parameter, test_parameters


class CRUD:
    def __init__(self):
        self.db = Connector()

    def create(self, entity_id: int , entity_type: str, comment: str,*, commit:bool = True, close:bool = True):
        """This method handles creating new rows in the data_notes table in the northwind foods database.
        The close argument decides whether to close the connection after running the method. By default, it is true
        The commit argument decides whether a change should be commited to the database immediately. By default, it is true.
        At present, the database can't handle customer ids, as they are not integers."""

        create_command = """\
        INSERT INTO data_notes (entity_id, entity_type, comment)
        VALUES (%s, %s, %s)
        """
        self.db.execute(create_command, (entity_id, entity_type, comment), commit=commit, close=close)

    def read(self,*, data_notes_id: int = None, entity_id: int = None, entity_type: str = None, limit: int = None, is_df: bool = False):
        """This method handles reading rows from the data_notes table.
        If no row id, entity id, entity type or limit is given, the function reads all rows.
        At present, it cannot filter by time."""
        sql = "SELECT * FROM data_notes"
        conditions = []
        parameters = {}
        test_parameters([data_notes_id, entity_id, entity_type],[int,int,str])
        if data_notes_id is not None:
            conditions.append("data_notes_id = %(data_notes_id)s")
            parameters["data_notes_id"] = data_notes_id

        if entity_id is not None:
            conditions.append("entity_id = %(entity_id)s")
            parameters["entity_id"] = entity_id

        if entity_type is not None:
            conditions.append("entity_type = %(entity_type)s")
            parameters["entity_type"] = entity_type

        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        sql += " ORDER BY created_at DESC"

        if limit is not None:
            sql +="\n LIMIT %(limit)s"
            parameters["limit"] = limit

        self.display_results(sql, parameters, is_df)

    def display_results(self, sql, parameters, is_df=False):
        self.db.connect()
        if is_df:
            print(self.db.query_as_df(sql, parameters))
        else:
            print(("data_notes_id", "data_notes_id", "entity_id", "entity_type", "created_at"))
            rows = self.db.query(sql, parameters)
            for row in rows:
                print(row)
        self.db.close()




    def update(self, *, data_notes_id: int, entity_id: int= None, entity_type: str = None, comment: str= None):
        """This method handles updates to the data_notes table. """
        sql = """UPDATE data_notes
        SET """
        updates = []
        parameters = {}
        test_parameters([data_notes_id, entity_id, entity_type, comment],[int,int,str,str])
        if entity_id is not None:
            updates.append("entity_id = %(entity_id)s")
            parameters["entity_type"] = entity_id

        if entity_type is not None:
            updates.append("entity_type = %(entity_type)s")
            parameters["entity_type"] = entity_type

        if comment is not None:
            updates.append("comment = %(comment)s")
            parameters["comment"] = comment

        if updates:
            sql += ", ".join(updates)

        sql += "\nWHERE data_notes_id = %(data_notes_id)s"
        parameters["data_notes_id"] = data_notes_id

        self.db.execute(sql, parameters)

    def delete(self,data_notes_id: int):
        """This method deletes a single row from the data_notes table based on the unique data_notes_id"""
        sql = """DELETE FROM data_notes
        WHERE data_notes_id = %(data_notes_id)s"""
        test_parameter(data_notes_id, int)
        parameters = {"data_notes_id": data_notes_id}
        self.db.execute(sql, parameters, commit = True)

    def delete_all_rows(self):
        """This method deletes all rows of the data_notes table.
        It is a nuclear option and should be handled with care."""
        input("Deleting all rows from database northwind")
        self.db.execute("TRUNCATE TABLE data_notes", commit = True)

    def set_up_table(self):
        """This method sets up the table data_notes if it does not exist. """

        table_command = """\
        CREATE TABLE IF NOT EXISTS public.data_notes
(
    data_notes_id integer NOT NULL DEFAULT nextval('data_notes_id_seq'::regclass),
    entity_id integer NOT NULL,
    entity_type character varying COLLATE pg_catalog."default" NOT NULL,
    comment character varying COLLATE pg_catalog."default",
    created_at timestamp with time zone DEFAULT now(),
    CONSTRAINT data_notes_id PRIMARY KEY (data_notes_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.data_notes
    OWNER to postgres;

COMMENT ON COLUMN public.data_notes.data_notes_id
    IS 'This is the primary key of the table.';

COMMENT ON COLUMN public.data_notes.entity_id
    IS 'This id should match the id of the product, order,  shipper etc. which the note refers to. ';

COMMENT ON COLUMN public.data_notes.entity_type
    IS 'This columns holds the entity type. This tells how to match the entity_id.';

COMMENT ON COLUMN public.data_notes.comment
    IS 'This column holds the comment created by the user.';

COMMENT ON COLUMN public.data_notes.created_at
    IS 'This holds the time when the row was created.';
    """
        self.db.execute(table_command, close=True, commit=True)
