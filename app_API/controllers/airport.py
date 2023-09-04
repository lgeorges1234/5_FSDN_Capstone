from flask import Blueprint, abort, jsonify, request
from sqlalchemy import or_

from app_API.auth.restricted_access import restrict_access
from ..models import Airport

#Instanciate a blueprint object
airport_bp = Blueprint('airport', __name__)


#---------------------------------------
#           Utility functions
#---------------------------------------

def get_airports(airport_code=None):
    airports_dict = {}
    if airport_code:
        airports_dict = Airport.query.get(airport_code)
    else:
        airports_dict = Airport.query.order_by(Airport.countryname, Airport.name).all()
    return airports_dict



#  GET Airport
#  ----------------------------------------------------------------

# Get Airports
@airport_bp.route('/airports')
@restrict_access
def retrieve_airports():
    try:
        airports = get_airports()
        return jsonify(
            {
                "success": True,
                "airports": [airport.format() for airport in airports]
            }
        )
    except:
        abort(422)


# Get Airport by code
@airport_bp.route('/airports/<string:airport_code>')
@restrict_access
def retrieve_airports_by_id(airport_code):
    try:
        airports = get_airports(airport_code)
        return jsonify(
            {
                "success": True,
                "airports": airports.format()
            }
        )
    except:
        abort(422)

# Get Airport by search term
@airport_bp.route('/airports', methods=['POST'])
@restrict_access
def retrieve_airports_by_search_terms(airport_id):
    body = request.get_json()
    search_term = body.get.searchTerm
    try:
        airports = Airport.query.filter(or_(Airport.name.ilike("%{}%".format(search_term)),
                                    Airport.countryname.ilike("%{}%".format(search_term)))
                               ).order_by(Airport.countryname, Airport.name).all()
        return jsonify(
            {
                "success": True,
                "airports": [airport.format() for airport in airports]
            }
        )
    except:
        abort(422)