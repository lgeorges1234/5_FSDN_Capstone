from flask import Blueprint, jsonify, abort, request
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from app_API.auth.auth import requires_auth

from app_API.auth.restricted_access import restrict_access
from ..models import Flight, Flight

#Instanciate a blueprint object
flight_bp = Blueprint('flight', __name__)


#---------------------------------------
#           Utility functions
#---------------------------------------

def get_flights(flight_id=None):
    print(flight_id)
    flights_dict = {}
    if flight_id:
        flights_dict = Flight.query.get(flight_id)
    else:
        flights_dict = Flight.query.order_by(Flight.country_id, Flight.name).all()
    return flights_dict



#  GET Flight
#  ----------------------------------------------------------------

# Get Flights
@flight_bp.route('/flights')
@requires_auth('get:flight')
def retrieve_flights():
    try:
        flights = get_flights()
        return jsonify(
            {
                "success": True,
                "flights": [flight.format() for flight in flights]
            }
        )
    except:
        abort(422)


# Get Flight by code
@flight_bp.route('/flights/<int:flight_id>')
@requires_auth('get:flight')
def retrieve_flights_by_id(flight_id):
    try:
        flights = get_flights(flight_id)
        return jsonify(
            {
                "success": True,
                "flights": flights.format()
            }
        )
    except:
        abort(422)


@flight_bp.route('/flights/search', methods=['POST'])
@requires_auth('get:flight')
def retrieve_flight_by_search_term():
    body = request.get_json()
    search_term = body.get("searchTerm", None)

    try:
        if search_term:
            flights = Flight.query.filter(or_(Flight.name.ilike("%{}%".format(search_term)),
                                        Flight.country_id.ilike("%{}%".format(search_term)))
                                ).order_by(Flight.country_id, Flight.name).all()
            return jsonify(
                {
                    "success": True,
                    "flights": [flight.format() for flight in flights]
                }
            )
        else:
            abort(422, "Missing search term")

    # except SQLAlchemyError as e:
    #     db.session.rollback()
    #     abort(500, "Database error")

    except Exception as e:
        abort(500, "Internal server error")


#  CREATE Flight
#  ----------------------------------------------------------------

    """
    Endpoint to CREATE a new flight, which will require a name and a country_id.
    The endpoint also allows to get an flight based on a search term.
    """

@flight_bp.route('/flights', methods=['POST'])
@requires_auth('create:flight')
def create_flight():
    body = request.get_json()
    name = body.get("name", None)
    country_id = body.get("country_id", None)
    search_term = body.get("searchTerm", None)

    try:
        if search_term:
            flights = Flight.query.filter(or_(Flight.name.ilike("%{}%".format(search_term)),
                                        Flight.country_id.ilike("%{}%".format(search_term)))
                                ).order_by(Flight.country_id, Flight.name).all()
            return jsonify(
                {
                    "success": True,
                    "flights": [flight.format() for flight in flights]
                }
            )
        elif name and country_id:
            flight = Flight(name=name, country_id=country_id)
            flight.insert()
            return jsonify(
                {
                    "success": True,
                    "flights": flight.format()
                }
            )
        else:
            abort(422)

    except:
        abort(422)


#  DELETE Flight
#  ----------------------------------------------------------------

@flight_bp.route("/flights/<int:flight_id>", methods=["DELETE"])
@requires_auth('delete:flight')
def delete_flight(flight_id):
    try:
        flight = Flight.query.filter(Flight.id==flight_id).one_or_none()
        flight.delete()
        return jsonify(
            {
                "success": True,
                "deleted": flight_id
            }
            ), 200
    except:
        abort(422)


#  PATCH Flight
#  ----------------------------------------------------------------
@flight_bp.route('/flights/<int:flight_id>', methods=["PATCH"])
@requires_auth('patch:flight')
def update_flight(upload, flight_id):
    try:
        body: request.get_json()

        if not body:
            abort(400)

        name = body.get('name', None)
        country_code = ('country_code', None)
        flight = Flight.query.filter(Flight.id == flight_id).one_or_more()

        if name:
            flight.name = name
        if country_code:
            flight.country_code = country_code
        
        flight.update()

        return jsonify({
            'success': True,
            'flights': flight
        })
    
    except Exception:
        abort(422) 


        


