from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import argparse

def import_airline():
    from app_API.models import Airline
    return Airline


def import_data(db_path):
    try:
        db_url = db_path

        # Create an engine and session
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        #Insert Country from the country.sql file
        with open('./app_API/SQL_files/country.sql', 'r') as file:
            sql_statements = file.read()
        sql_statements = sql_statements.split(';')
        for statement in sql_statements:
            if statement.strip():  # Skip empty statements
                session.execute(statement)

        #Insert Airports from the airport.sql file
        with open('./app_API/SQL_files/airport.sql', 'r') as file:
            sql_statements = file.read()
        sql_statements = sql_statements.split(';')
        for statement in sql_statements:
            if statement.strip():  # Skip empty statements
                session.execute(statement)

        #Insert Status from the flightStatus.sql file
        with open('./app_API/SQL_files/flightStatus.psql', 'r') as file:
            sql_statements = file.read()
        sql_statements = sql_statements.split(';')
        for statement in sql_statements:
            if statement.strip():  # Skip empty statements
                session.execute(statement)

        # Create a new Airline object
        Airline = import_airline()
        airline = Airline(name='Airfrance', country_code='FR')
        # Add the object to the session
        session.add(airline)

        # Commit the changes to the database
        session.commit()
        # Close the session
        session.close()
    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {str(e)}")    
