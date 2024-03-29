from resources.database import Database
import logging
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text


def create_tables(model):
    db = Database()
    engine = db.create_engine()
    try:
        db.Base.metadata.create_all(bind=engine,
                                    tables=[model.__table__])
    except ProgrammingError as e:
        logging.error(f"An error occurred while creating tables.\nError: {str(e)}\n")
        raise


def drop_table(model):
    db = Database()
    engine = db.create_engine()
    try:
        db.Base.metadata.drop_all(bind=engine, tables=[model.__table__])
    except Exception as e:
        logging.error(f"An error occurred while dropping tables.\nError: {str(e)}\n")
        raise


def delete_records(model):
    db = Database()
    session = db.create_session()
    try:
        session.query(model).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"An error occurred while deleting the records.\nError: {str(e)}\n")
        raise
    finally:
        session.close()


def insert_data(data):
    db = Database()
    session = db.create_session()
    try:

        if type(data) == list:
            for each_data in data:
                session.add(each_data)
            session.commit()
        else:
            session.add(data)
            session.commit()

    except Exception as e:
        session.rollback()
        logging.error(f"An error occurred.\nError: {str(e)}\n")
        raise
    finally:
        session.close()


def call_stored_procedure(schema, procedure_name):
    """
    Calls the specified stored procedure using the current database engine.

    :param schema: The name of the schema where the procedure is stored
    :param procedure_name: The name of the stored procedure to call
    """
    db = Database()
    session = db.create_session()

    session.execute(text(f"EXEC {schema}.{procedure_name}"))
    session.commit()
    db.close_session(session)
