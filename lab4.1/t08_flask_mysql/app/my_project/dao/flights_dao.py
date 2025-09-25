from t08_flask_mysql.app.my_project.db import db
from sqlalchemy import text
from t08_flask_mysql.app.my_project.domain.flights import Flight

class FlightsDAO:
    @staticmethod
    def get_all_flights():
        return Flight.query.all()

    @staticmethod
    def get_flight_by_id(flight_id):
        return Flight.query.get(flight_id)

    @staticmethod
    def create_flight(flight_data):
        flight = Flight(**flight_data)
        db.session.add(flight)
        db.session.commit()
        return flight

    @staticmethod
    def update_flight(flight_id, flight_data):
        flight = Flight.query.get(flight_id)
        if flight:
            for key, value in flight_data.items():
                setattr(flight, key, value)
            db.session.commit()
        return flight

    @staticmethod
    def delete_flight(flight_id):
        flight = Flight.query.get(flight_id)
        if flight:
            db.session.delete(flight)
            db.session.commit()
            return True
        return False


    @staticmethod
    def get_flight_crew_assignments():
        query = text("""
            SELECT 
                fca.crew_id,
                fca.flight_id,
                c.name AS crew_member_name,
                c.position AS crew_member_position,
                f.flight_number,
                f.departure_time,
                f.arrival_time
            FROM 
                FlightCrewAssignments fca
            JOIN 
                Crew c ON fca.crew_id = c.id
            JOIN 
                Flights f ON fca.flight_id = f.id;
        """)
        result = db.session.execute(query)
        return result.fetchall()