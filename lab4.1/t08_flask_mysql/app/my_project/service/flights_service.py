from t08_flask_mysql.app.my_project.dao.flights_dao import FlightsDAO

class FlightsService:
    @staticmethod
    def get_all_flights():
        return FlightsDAO.get_all_flights()

    @staticmethod
    def get_flight_by_id(flight_id):
        return FlightsDAO.get_flight_by_id(flight_id)

    @staticmethod
    def create_flight(flight_data):
        return FlightsDAO.create_flight(flight_data)

    @staticmethod
    def update_flight(flight_id, flight_data):
        return FlightsDAO.update_flight(flight_id, flight_data)

    @staticmethod
    def delete_flight(flight_id):
        return FlightsDAO.delete_flight(flight_id)

    @staticmethod
    def get_flight_crew_assignments():
        return FlightsDAO.get_flight_crew_assignments()
