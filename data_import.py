from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import argparse

from models import Airlines

# Retrieve the database url from args passed to the call
parser = argparse.ArgumentParser()
parser.add_argument('--db-url', help='Database URL')
args = parser.parse_args()
db_url = args.db_url

# Create an engine and session
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()


# Create a new Airline object
airline = Airlines(name='Airfrance', country_id='FR')
# Add the object to the session
session.add(airline)

#Insert Airports from the airport.sql file
# Read the SQL file
with open('airport.sql', 'r') as file:
    sql_statements = file.read()

# Split the SQL statements
sql_statements = sql_statements.split(';')

# Execute the SQL statements
for statement in sql_statements:
    if statement.strip():  # Skip empty statements
        session.execute(statement)


# Commit the changes to the database
session.commit()
# Close the session
session.close()

