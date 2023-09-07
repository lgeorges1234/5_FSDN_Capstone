from .flight import flight_bp
from .airline import airline_bp
from .airport import airport_bp
from .country import country_bp

# Export the blueprints
__all__ = ['flight_bp', 'airline_bp', 'airport_bp', 'country_bp']