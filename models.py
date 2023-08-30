import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import Column, String, ForeignKey, Integer, String, DateTime, create_engine
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
import subprocess

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

# database_path = os.environ['DATABASE_URL']
# if database_path.startswith("postgres://"):
#   database_path = database_path.replace("postgres://", "postgresql://", 1)

posgres_host = os.getenv("POSTGRES_HOST")
posgres_port = os.getenv("PORT_DEV")
database_name = os.getenv("POSTGRES_DB_DEV")
user_name = os.getenv("POSTGRES_USER_DEV")
user_password = os.getenv("POSTGRES_PASSWORD_DEV")

database_path = f'postgresql://{user_name}:{user_password}@{posgres_host}:{posgres_port}/{database_name}'

db = SQLAlchemy()

def import_data():
    try:
      # Run a command and capture the output
      result = subprocess.run(['python', 'data_import.py', '--db-url', database_path], capture_output=True, text=True, check=True)

      # Print the output
      print(result.stdout)

    except subprocess.CalledProcessError as e:
        # Handle the error if the command fails
        print(f"Command failed with return code {e.returncode}:")
        print(e.stderr)

    except Exception as e:
        # Handle any other exceptions
        print(f"An error occurred: {str(e)}")

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    import_data()


'''
Passenger
'''
class Passenger(db.Model):  
  __tablename__ = 'Passenger'

  id = Column(db.Integer, primary_key=True)
  firstname = Column(String)
  lastname = Column(String)

  def __init__(self, firstname, lastname):
    self.firstname = firstname
    self.lastname = lastname

  def format(self):
    return {
      'id': self.id,
      'firstname': self.firstname,
      'lastname': self.lastname}


class Flight(db.Model):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    flightname = Column(String(20), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    departure = Column(String(20), ForeignKey('airports.code'))
    arrival = Column(String(20), ForeignKey('airports.code'))
    status = Column(Integer, ForeignKey('flightStatus.id'), nullable=False)
    airline_id = Column(Integer, ForeignKey('airlines.id'), nullable=False)

    # Define relationships with other tables
    departure_airport = relationship("Airport", foreign_keys=[departure])
    arrival_airport = relationship("Airport", foreign_keys=[arrival])
    flight_status = relationship("FlightStatus")
    airline = relationship("Airline")
  
    def __init__(self, flightname, date, departure, arrival, status, airline_id):
      self.id = id
      self.flightname = flightname,
      self.date = date,
      self.departure = departure,
      self.arrival = arrival,
      self.status = status,
      self.airline_id = airline_id

    def format(self):
      return {
        'id': self.id,
        'flightname': self.flightname,
        'date' : self.date,
        'departure' : self.departure,
        'arrival' : self.arrival,
        'status' : self.status,
        'airline_id' : self.airline_id
        }


class Airlines(db.Model):
    __tablename__ = 'airlines'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_id = db.Column(db.String(64), db.ForeignKey('countries.id'), nullable=False)

    # Define relationship with the countries table
    country = db.relationship("Countries")


from flask_sqlalchemy import SQLAlchemy


class Airport(db.Model):
    __tablename__ = 'airports'

    name = db.Column(db.String(56))
    code = db.Column(db.String(3), primary_key=True)
    stateCode = db.Column(db.String(2))
    countryCode = db.Column(db.String(2))
    countryName = db.Column(db.String(32))