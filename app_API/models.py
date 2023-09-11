import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import Column, String, ForeignKey, Integer, String, DateTime, create_engine
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
import logging



from app_API.data_import import import_data

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

# Enable SQLAlchemy logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.drop_all() 
    db.create_all()
    import_data(database_path)


class Country(db.Model):
   __tablename__ = 'countries'
   code = db.Column(db.String(3), primary_key=True)
   name = db.Column(db.String(100))

   # Define the relationship with the Airport and Airline tables
   airports = db.relationship("Airport", backref="countries_airports", lazy=True)
   airlines = db.relationship("Airline", backref="countries_airlines", lazy=True)

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
    passenger_id = Column(String(64), nullable=False)

    # Define relationships with other tables
    departure = relationship("Airport", foreign_keys=[departure_code], backref="departures")
    arrival = relationship("Airport", foreign_keys=[arrival_code], backref="arrivals")
    flight_status = relationship("Flightstatus")
    airline = relationship("Airline")

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
  
    def __init__(self, flightname, date, departure_code, arrival_code, status, airline_id, passenger_id):
        self.flightname = flightname
        self.date = date
        self.departure_code = departure_code
        self.arrival_code = arrival_code
        self.status = status
        self.airline_id = airline_id
        self.passenger_id = passenger_id

    def format(self):
      return {
        'id': self.id,
        'flightname': self.flightname,
        'date' : self.date,
        'departure_code' : self.departure_code,
        'arrival_code' : self.arrival_code,
        'status' : self.status,
        'airline_id' : self.airline_id
        }


class Airline(db.Model):
    __tablename__ = 'airlines'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), nullable=False)
    country_code = db.Column(String(64), db.ForeignKey('countries.code'), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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

    def format(self):
      return {
        'name': self.name,
        'code': self.code,
        'statecode' : self.statecode,
        'countrycode' : self.countrycode,
        'countryname' : self.countryname,
        }