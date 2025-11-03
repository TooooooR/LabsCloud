from ..controller.airlines_controller import airlines_bp, airlines_bpp
from ..controller.airplanes_controlle import airplanes_bp, airplanes_detailed_bp, flights_crew_bpp, airplanes_bpp, airplanes_max, airplanes_random
from ..controller.flights_controller import flights_bp, flights_crew_bp


def register_routes(app):
    app.register_blueprint(airlines_bp, url_prefix='/airlines')
    app.register_blueprint(airplanes_bp, url_prefix='/airplanes')
    app.register_blueprint(flights_bp, url_prefix='/flights')
    app.register_blueprint(airplanes_detailed_bp, url_prefix='/airplanes/details')
    app.register_blueprint(flights_crew_bp, url_prefix='/flights/details')
    app.register_blueprint(flights_crew_bpp, url_prefix='/flights/in')
    app.register_blueprint(airplanes_bpp, url_prefix='/airplanes/insert')
    app.register_blueprint(airlines_bpp, url_prefix='/airlines/dummy')
    app.register_blueprint(airplanes_max, url_prefix='/airplanes/max_hour')
    app.register_blueprint(airplanes_random, url_prefix='/airplanes/random')


    