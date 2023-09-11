from flask import Blueprint, jsonify, abort, request
from sqlalchemy import or_
from datetime import date

from app_API.auth.auth import get_token_auth_header, requires_auth, verify_decode_jwt
from app_API.auth.restricted_access import restrict_access
from ..models import Flight

#Instanciate a blueprint object
flight_bp = Blueprint('flight', __name__)

#---------------------------------------
#           Utility functions
#---------------------------------------

def get_flights(flight_id=None):
    flights_dict = {}
    if flight_id:
        flights_dict = Flight.query.get(flight_id)
    else:
        flights_dict = Flight.query.order_by(Flight.date).all()
    return flights_dict

def get_passenger_id():
    token = get_token_auth_header()
    payload = verify_decode_jwt(token)
    passenger_id = payload['sub']
    return passenger_id

def get_current_date():
    current_date = date.today()
    formatted_date = current_date.strftime('%Y-%m-%d')
    return formatted_date

#  GET Flight
#  ----------------------------------------------------------------

# Get Flights
@flight_bp.route('/flights')
@requires_auth('get:flights')
def retrieve_flights(payload):
    try:
        flights = get_flights()
        return jsonify(
            {
                "success": True,
                "flights": [flight.format() for flight in flights]
            }
        )
    except Exception as e:
        # print(e)
        abort(422)




#  CREATE Flight
#  ----------------------------------------------------------------

    """
    Endpoint to CREATE a new flight, which will require a name and a country_code.
    The endpoint also allows to get an flight based on a search term.
    """

@flight_bp.route('/flights', methods=['POST'])
@requires_auth('post:flights')
def create_flight(payload):
    body = request.get_json()
    flightname = body.get("flightname", None)
    date = get_current_date()
    departure_code = body.get("departure_code", None)
    arrival_code = body.get("arrival_code", None)
    status = body.get("status", None)
    airline_id = body.get("airline_id", None)
    passenger_id = get_passenger_id()

    try:
        if flightname and date and departure_code and arrival_code and status and airline_id and passenger_id:
            flight = Flight(flightname=flightname, date=date, departure_code=departure_code, arrival_code=arrival_code, status=status, airline_id=airline_id, passenger_id=passenger_id)
            flight.insert()
            return jsonify(
                    {
                        "success": True,
                        "flights": [flight.format()]
                    }
                )
        else:
            abort(422)

    except Exception as e:
        abort(422)



