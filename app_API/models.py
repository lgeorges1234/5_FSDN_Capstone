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
      result = subprocess.run(['python', './app_API/data_import.py', '--db-url', database_path], capture_output=True, text=True, check=True)

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
    print("database_path : " + str(database_path))
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.drop_all() 
    db.create_all()
    import_data()


'''
Passenger
'''
class Passenger(db.Model):  
  __tablename__ = 'passengers'

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

class Country(db.Model):
   __tablename__ = 'countries'
   code = db.Column(db.String(3), primary_key=True)
   name = db.Column(db.String(100))

   # Define the relationship with the Airport table
   airports = db.relationship("Airport", backref="countries_airports")
   airlines = db.relationship("Airline", backref="countries_airlines")

   def format(self):
    return {
      'code': self.code,
      'name': self.name
      }

class Flightstatus(db.Model):
   __tablename__ = 'flightstatus'

   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20))

   def format(self):
    return {
      'id': self.id,
      'name': self.name
      }

class Flight(db.Model):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    flightname = Column(String(20), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    departure_code = Column(String(20), ForeignKey('airports.code'))
    arrival_code = Column(String(20), ForeignKey('airports.code'))
    status = Column(Integer, ForeignKey('flightstatus.id'), nullable=False)
    airline_id = Column(Integer, ForeignKey('airlines.id'), nullable=False)

    # Define relationships with other tables
    departure = relationship("Airport", foreign_keys=[departure_code])
    arrival = relationship("Airport", foreign_keys=[arrival_code])
    flight_status = relationship("Flightstatus")
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


class Airline(db.Model):
    __tablename__ = 'airlines'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    country_code = db.Column(String(64), db.ForeignKey('countries.code'), nullable=False)

    # Define relationships with other tables
    # countrycode = relationship("Country", foreign_keys=[country_code],lazy=True)

    def format(self):
      return {
        'id': self.id,
        'name': self.name,
        'country_code': self.country_code,
        }

class Airport(db.Model):
    __tablename__ = 'airports'

    name = db.Column(db.String(56))
    code = db.Column(db.String(3), primary_key=True)
    statecode = db.Column(db.String(2))
    countrycode = db.Column(db.String(2), db.ForeignKey('countries.code'), nullable=False)
    countryname = db.Column(db.String(32))

    # Define relationships with other tables
    # country = relationship("Country", foreign_keys=[countrycode])
    # country = relationship("Country", backref="airports")

    def format(self):
      return {
        'name': self.name,
        'code': self.code,
        'statecode' : self.statecode,
        'countrycode' : self.countrycode,
        'countryname' : self.countryname,
        }