from flask import Blueprint, jsonify, abort, request
from sqlalchemy import or_


from app_API.auth.auth import requires_auth
from app_API.auth.restricted_access import restrict_access
from ..models import Airline

#Instanciate a blueprint object
airline_bp = Blueprint('airline', __name__)

#---------------------------------------
#           Utility functions
#---------------------------------------

def get_airlines(airline_id=None):
    airlines_dict = {}
    if airline_id:
        airlines_dict = Airline.query.get(airline_id)
    else:
        airlines_dict = Airline.query.order_by(Airline.country_code, Airline.name).all()
    return airlines_dict



#  GET Airline
#  ----------------------------------------------------------------

# Get Airlines
@airline_bp.route('/airlines')
@requires_auth('get:airlines')
def retrieve_airlines(payload):
    try:
        airlines = get_airlines()
        return jsonify(
            {
                "success": True,
                "airlines": [airline.format() for airline in airlines]
            }
        )
    except Exception as e:
        abort(422)


# Get Airline by id
@airline_bp.route('/airlines/<int:airline_id>')
@requires_auth('get:airlines')
def retrieve_airlines_by_id(payload, airline_id):
    try:
        airlines = get_airlines(airline_id)
        return jsonify(
            {
                "success": True,
                "airlines": [airlines.format()]
            }
        )
    except Exception as e:
        abort(422)

# Get Airline by search term
@airline_bp.route('/airlines-search', methods=['POST'])
@requires_auth('get:airlines')
def retrieve_airlines_by_search_term(payload):
    body = request.get_json()
    search_term = body.get("searchTerm", None)
    try:
        if search_term:
            # airlines = Airline.query.join(Country,Airline.country_code == Country.code).filter(or_(Airline.name.ilike("%{}%".format(search_term)),
            #                             Country.name.ilike("%{}%".format(search_term)))
            #                     ).order_by(Airline.country_code, Airline.name).all()
            airlines = Airline.query.join(Country, Airline.country_code == Country.code)\
                .filter(or_(Airline.name.ilike("%{}%".format(search_term)),
                Country.name.ilike("%{}%".format(search_term))))\
    .order_by(Airline.country_code, Airline.name).all()
            return jsonify(
                {
                    "success": True,
                    "airlines": [airline.format() for airline in airlines]
                }
            )
        else:
            abort(422)

    except Exception as e:
        abort(422)


#  CREATE Airline
#  ----------------------------------------------------------------

    """
    Endpoint to CREATE a new airline, which will require a name and a country_code.
    The endpoint also allows to get an airline based on a search term.
    """

@airline_bp.route('/airlines', methods=['POST'])
@requires_auth('post:airlines')
def create_airline(payload):
    body = request.get_json()
    name = body.get("name", None)
    country_code = body.get("country_code", None)

    try:
        if name and country_code:
            airline = Airline(name=name, country_code=country_code)
            airline.insert()
            return jsonify(
                {
                    "success": True,
                    "airlines": [airline.format()]
                }
            )
        else:
            abort(422)

    except Exception as e:
        abort(422)



#  PATCH Airline
#  ----------------------------------------------------------------
@airline_bp.route('/airlines/<int:airline_id>', methods=["PATCH"])
@requires_auth('patch:airlines')
def update_airline(payload, airline_id):
    try:
        body = request.get_json()
        if not body:
            abort(400)

        name = body.get('name', None)
        country_code = body.get('country_code', None)
        
        airline = get_airlines(airline_id)
        if name:
            airline.name = name
        if country_code:
            airline.country_code = country_code
        
        airline.update()

        return jsonify({
            'success': True,
            "airlines": [airline.format()]
        })
    
    except Exception as e:
        abort(422) 


#  DELETE Airline
#  ----------------------------------------------------------------

@airline_bp.route("/airlines/<int:airline_id>", methods=["DELETE"])
@requires_auth('delete:airlines')
def delete_airline(payload, airline_id):
    try:
        airline = get_airlines(airline_id)
        airline.delete()
        return jsonify(
            {
                "success": True,
                "deleted": airline_id
            }
            ), 200
    except Exception as e:
        abort(422)       


