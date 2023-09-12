import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from app_API.models import setup_db

from dotenv import load_dotenv
from pathlib import Path

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

posgres_host = os.getenv("POSTGRES_HOST")
posgres_port = os.getenv("PORT_DEV")
database_name = os.getenv("POSTGRES_DB_TEST")
user_name = os.getenv("POSTGRES_USER_TEST")
user_password = os.getenv("POSTGRES_PASSWORD_TEST")

manager_token = os.getenv("MANAGER_TOKEN")
passenger_token = os.getenv("PASSENGER_TOKEN")


class FSDNTestCase(unittest.TestCase):
    """This class represents the FSDN test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = f'postgresql://{user_name}:{user_password}@{posgres_host}:{posgres_port}/{database_name}'

        test_config = {
            'DATABASE_URI': self.database_path
        }

        self.app = create_app(test_config['DATABASE_URI'])
        self.client = self.app.test_client

        setup_db(self.app, self.database_path)

        self.new_airline = {
            "name": "Lufthansa",
            "country_code": "DE",
            }
        
        self.bad_formated_airlines = {
            "name": "Lufthansa",
            "country_id": "DE",
            }
        
        self.new_flight = {
            "flightname": "DC708",
            "departure_code": "AHC",
            "arrival_code": "AGH",
            "status": "0",
            "airline_id": 1,
            }

        self.bad_formated_flight = {
            "flightname": "DC708",
            "departure": "AHC",
            "arrival_code": "AGH",
            "status": "0",
            "airline_id": 1,
            }



        self.headers_manager = {
            'Authorization': f'Bearer {manager_token}'
        }

        self.headers_passenger = {
            'Authorization': f'Bearer {passenger_token}'
        }
        

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_server(self):

        res = self.client().get("/")
        self.assertEqual(res.status_code, 200)


#---------------------------------------
#           Airport Endpoint Tests
#---------------------------------------

#  GET Airport
#  ----------------------------------------------------------------

    def test_get_airports(self):

        res = self.client().get("/airports", headers=self.headers_manager)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["airports"])

    def test_get_airports_by_id(self):

        res = self.client().get("/airports/AUU", headers=self.headers_manager)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["airports"]["code"], "AUU")
    
    def test_404_get_airports_by_numerical_id(self):

        res = self.client().get("/airports/123", headers=self.headers_manager)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")

    def test_get_airports_by_searchTerm(self):

        res = self.client().post("/airports", json={"searchTerm":"France"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["airports"]) > 0)

    def test_get_airports_by_searchTerm_without_results(self):

        res = self.client().post("/airports", json={"searchTerm":"lubilidae"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["airports"]), 0)

#---------------------------------------------------------------
#                   Airline Endpoint Tests
#---------------------------------------------------------------

#  GET Airline
#  ----------------------------------------------------------------

    def test_get_airlines(self):

        res = self.client().get("/airlines", headers=self.headers_passenger)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["airlines"])

    def test_get_airlines_by_id(self):

        res = self.client().get("/airlines/1", headers=self.headers_manager)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["airlines"][0]["country_code"], "FR")
    
    def test_404_get_airports_by_nom_numerical_id(self):

        res = self.client().get("/airlines/AUU", headers=self.headers_manager)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

    def test_get_airlines_by_searchTerm(self):

        res = self.client().post("/airlines-search", headers=self.headers_manager, json={"searchTerm":"France"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["airlines"][0]["country_code"], "FR")

    def test_get_airlines_by_searchTerm_without_results(self):

        res = self.client().post("/airlines-search", headers=self.headers_manager, json={"searchTerm":"lubilidae"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data["airlines"]), 0)

#  CREATE Airline
#  ----------------------------------------------------------------

    def test_create_new_airline(self):
        res = self.client().post("/airlines", headers=self.headers_manager, json=self.new_airline)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["airlines"][0]["country_code"], "DE")

    def test_403_create_new_airline_without_right_permissions(self):
        res = self.client().post("/airlines", headers=self.headers_passenger, json=self.new_airline)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]["description"], "Permission not found.")

    def test_422_if_airline_creation_fails(self):
        res = self.client().post("/airlines", headers=self.headers_manager, json=self.bad_formated_airlines)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")


#  UPDATE Airline
#  ----------------------------------------------------------------

    def test_update_airline(self):
        res = self.client().patch("/airlines/1", headers=self.headers_manager, json={"country_code":"AU"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["airlines"][0]["country_code"], "AU")

    def test_403_update_airline_without_right_permissions(self):
        res = self.client().patch("/airlines/1", headers=self.headers_passenger, json={"country_code":"FR"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]["description"], "Permission not found.")

    # def test_422_if_airline_update_badly_formated(self):
    #     res = self.client().patch("/airlines/1", headers=self.headers_manager, json={"country_code":1})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "Unprocessable")
    
    def test_422_if_airline_update_fails(self):
        res = self.client().patch("/airlines/10", headers=self.headers_manager, json={"country_code":1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")

#  DELETE Airline
#  ----------------------------------------------------------------

    def test_airline_delete(self):
        res = self.client().delete("/airlines/1", headers=self.headers_manager)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 1)

    def test_422_if_airline_delete_fails(self):
        res = self.client().delete("/airlines/10", headers=self.headers_manager)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")


#---------------------------------------------------------------
#                   Country Endpoint Tests
#---------------------------------------------------------------

#  GET Countrie
#  ----------------------------------------------------------------

    def test_get_countries(self):

        res = self.client().get("/countries")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


#---------------------------------------------------------------
#                   Flight Endpoint Tests
#---------------------------------------------------------------


#  CREATE Flight
#  ----------------------------------------------------------------

    def test_create_new_flight(self):
        res = self.client().post("/flights", headers=self.headers_passenger, json=self.new_flight)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["flights"][0]["flightname"], "DC708")


    def test_403_create_flight_without_right_permissions(self):
        res = self.client().post("/flights", headers=self.headers_manager, json=self.new_flight)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"]["description"], "Permission not found.")

    def test_422_if_flight_create_flight_fails(self):
        res = self.client().post("/flights", headers=self.headers_passenger, json=self.bad_formated_flight)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable")

#  GET Flight
#  ----------------------------------------------------------------

    def test_get_flight(self):
        self.client().post("/flights", headers=self.headers_passenger, json=self.new_flight)
        res = self.client().get("/flights", headers=self.headers_manager)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["flights"][0]["flightname"], "DC708")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


# python3 test_flasker.py --verbose