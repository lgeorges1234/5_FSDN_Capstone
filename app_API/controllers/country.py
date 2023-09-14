from flask import Blueprint, abort, jsonify, request
from sqlalchemy import or_

from app_API.auth.restricted_access import restrict_access
from ..models import Country

#Instanciate a blueprint object
country_bp = Blueprint('country', __name__)


#---------------------------------------
#           Utility functions
#---------------------------------------

def get_countries(country_code=None):
    countries_dict = {}
    if country_code:
        countries_dict = Country.query.get(country_code)
    else:
        countries_dict = Country.query.order_by(Country.name).all()
    return countries_dict



#  GET Country
#  ----------------------------------------------------------------

# Get Countrys
@country_bp.route('/countries')
# @restrict_access
def retrieve_countries():
    try:
        countries = get_countries()
        return jsonify(
            {
                "success": True,
                "countries": [country.format() for country in countries]
            }
        )
    except:
        abort(422)


# Get Country by code
@country_bp.route('/countries/<string:country_code>')
# @restrict_access
def retrieve_countries_by_id(country_code):
    try:
        countries = get_countries(country_code)
        return jsonify(
            {
                "success": True,
                "countries": countries.format()
            }
        )
    except:
        abort(422)

# Get Country by search term
@country_bp.route('/countries', methods=['POST'])
# @restrict_access
def retrieve_countries_by_search_terms(country_id):
    body = request.get_json()
    search_term = body.get.searchTerm
    try:
        countries = Country.query.filter(Country.name.ilike("%{}%".format(search_term))
                               ).order_by(Country.code, Country.name).all()
        return jsonify(
            {
                "success": True,
                "countries": [country.format() for country in countries]
            }
        )
    except:
        abort(422)