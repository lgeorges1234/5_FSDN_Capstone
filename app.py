from flask import Flask,  jsonify
from app_API.models import setup_db
from flask_cors import CORS

from app_API.controllers import airport_bp, airline_bp, flight_bp, country_bp
from app_API.auth.auth import AuthError, requires_auth

#---------------------------------------
#           Utility functions
#---------------------------------------




#---------------------------------------
#           Flask App
#---------------------------------------

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    if test_config:
        setup_db(app, test_config)
    else:
        setup_db(app)


    """
    Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)

    """
    set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response


    @app.route('/')
    def check_server():
        return "server running"
    
    # """
    # Endpoints to handle Passenger
    # """

    # app.route('/passenger/<int:passenger_id>')
    # def search_by_passenger(passenger_id):
    #     try:
    #         passenger = Passenger.query.filter(passenger_id).one_or_none()
    #         return jsonify(
    #             {
    #                 "success": True,
    #                 "passenger": passenger.format()
    #             }
    #         )
    #     except:
    #         abort(422)



#  ----------------------------------------------------------------
#  Airports
#  ----------------------------------------------------------------
    app.register_blueprint(airport_bp)


#  ----------------------------------------------------------------
#  Airlines
#  ----------------------------------------------------------------
    app.register_blueprint(airline_bp)


#  ----------------------------------------------------------------
#  Flights
#  ----------------------------------------------------------------
    app.register_blueprint(flight_bp)


#  ----------------------------------------------------------------
#  Counries
#  ----------------------------------------------------------------
    app.register_blueprint(country_bp)


#  ----------------------------------------------------------------
#  Error Handler
#  ----------------------------------------------------------------

    @app.errorhandler(400)
    def invalid_request(error):
        return (
                jsonify({
                    "success": False,
                    "error": 400,
                    "message": "Invalid request"
                    }), 400
        )

    @app.errorhandler(AuthError)
    def authentication_failed(error):
        """Handles authentication failed error (403)"""
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    @app.errorhandler(404)
    def not_found(error):
        return (
                jsonify({
                    "success": False,
                    "error": 404,
                    "message": "Resource not found"
                    }), 404
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
                jsonify({
                    "success": False,
                    "error": 422,
                    "message": "Unprocessable"
                    }), 422
        )

    @app.errorhandler(500)
    def internal_error(error):
        return (
                jsonify({
                    "success": False,
                    "error": 500,
                    "message": "Internal Server Error"
                    }), 500
        )

    return app

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

app = create_app()

if __name__ == '__main__':
    app.run()
