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
    print(airline_id)
    airlines_dict = {}
    if airline_id:
        airlines_dict = Airline.query.get(airline_id)
    else:
        airlines_dict = Airline.query.order_by(Airline.country_id, Airline.name).all()
    return airlines_dict



#  GET Airline
#  ----------------------------------------------------------------

# Get Airlines
@airline_bp.route('/airlines')
@restrict_access
def retrieve_airlines():
    try:
        airlines = get_airlines()
        return jsonify(
            {
                "success": True,
                "airlines": [airline.format() for airline in airlines]
            }
        )
    except:
        abort(422)


# Get Airline by code
@airline_bp.route('/airlines/<int:airline_id>')
@restrict_access
def retrieve_airlines_by_id(airline_id):
    try:
        airlines = get_airlines(airline_id)
        return jsonify(
            {
                "success": True,
                "airlines": airlines.format()
            }
        )
    except:
        abort(422)



#  CREATE Airline
#  ----------------------------------------------------------------

    """
    Endpoint to CREATE a new airline, which will require a name and a country_id.
    The endpoint also allows to get an airline based on a search term.
    """

@airline_bp.route('/airlines', methods=['POST'])
@requires_auth('create:airline')
def create_airline():
    body = request.get_json()
    name = body.get("name", None)
    country_id = body.get("country_id", None)
    search_term = body.get("searchTerm", None)

    try:
        if search_term:
            airlines = Airline.query.filter(or_(Airline.name.ilike("%{}%".format(search_term)),
                                        Airline.country_id.ilike("%{}%".format(search_term)))
                                ).order_by(Airline.country_id, Airline.name).all()
            return jsonify(
                {
                    "success": True,
                    "airlines": [airline.format() for airline in airlines]
                }
            )
        elif name and country_id:
            airline = Airline(name=name, country_id=country_id)
            airline.insert()
            return jsonify(
                {
                    "success": True,
                    "airlines": airline.format()
                }
            )
        else:
            abort(422)

    except:
        abort(422)


#  DELETE Airline
#  ----------------------------------------------------------------

@airline_bp.route("/airlines/<int:airline_id>", methods=["DELETE"])
@requires_auth('delete:airline')
def delete_airline(airline_id):
    try:
        airline = Airline.query.filter(Airline.id==airline_id).one_or_none()
        airline.delete()
        return jsonify(
            {
                "success": True,
                "deleted": airline_id
            }
            ), 200
    except:
        abort(422)


#  PATCH Airline
#  ----------------------------------------------------------------
@airline_bp.route('/airlines/<int:airline_id>', methods=["PATCH"])
@requires_auth('patch:airline')
def update_airline(upload, airline_id):
    try:
        body: request.get_json()

        if not body:
            abort(400)

        name = body.get('name', None)
        country_code = ('country_code', None)
        airline = Airline.query.filter(Airline.id == airline_id).one_or_more()

        if name:
            airline.name = name
        if country_code:
            airline.country_code = country_code
        
        airline.update()

        return jsonify({
            'success': True,
            'airlines': airline
        })
    
    except Exception:
        abort(422) 


        


