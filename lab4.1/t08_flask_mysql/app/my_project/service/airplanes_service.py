from ..dao.airplanes_dao import AirplanesDAO
from ..domain.airplanes import Airplane
from sqlalchemy import text
from ..db import db
from sqlalchemy.exc import SQLAlchemyError

class AirplanesService:
    @staticmethod
    def get_all_airplanes():
        return AirplanesDAO.get_all_airplanes()

    @staticmethod
    def get_airplane_by_id(airplane_id):
        return AirplanesDAO.get_airplane_by_id(airplane_id)

    @staticmethod
    def create_airplane(registration_number, model, total_flight_hours, airline_id):
        return AirplanesDAO.create_airplane(registration_number, model, total_flight_hours, airline_id)

    @staticmethod
    def update_airplane(airplane_id, registration_number, model, total_flight_hours, airline_id):
        return AirplanesDAO.update_airplane(airplane_id, registration_number, model, total_flight_hours, airline_id)

    @staticmethod
    def delete_airplane(airplane_id):
        return AirplanesDAO.delete_airplane(airplane_id)

    @staticmethod
    def get_all_airplanes_detailed():
        return AirplanesDAO.get_all_airplanes_detailed()

    @staticmethod
    def insert_flight_crew(flight_number, crew_name):
        sql = text("""
            CALL insert_flight_crew(:flight_number, :crew_name)
        """)
        try:
            result = db.session.execute(sql, {
                'flight_number': flight_number,
                'crew_name': crew_name
            })
            db.session.commit()
            return {"message": "Flight crew assigned successfully"}
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemyError: {str(e)}")
            return {"error": "Failed to assign crew to flight"}

    @staticmethod
    def insert_airplane(registration_number, model, total_flight_hours, airline_id):
        result = AirplanesDAO.call_insert_airplane(registration_number, model, total_flight_hours, airline_id)
        if result is True:
            return {"message": "Airplane inserted successfully"}
        else:
            # Розпізнаємо SQL помилки
            if "Airline ID does not exist" in result:
                return {"error": "Airline ID does not exist"}, 400
            else:
                return {"error": "Failed to insert airplane"}, 500

    @staticmethod
    def get_max_flight_hours_airplane():
        airplane_data = AirplanesDAO.get_max_flight_hours_airplane()

        if isinstance(airplane_data, dict) and "error" in airplane_data:
            return airplane_data, 500

        # Формуємо відповідь у JSON-форматі
        if airplane_data:
            airplane = airplane_data[0]
            return {
                "id": airplane.id,
                "registration_number": airplane.registration_number,
                "model": airplane.model,
                "total_flight_hours": airplane.total_flight_hours
            }, 200
        else:
            return {"message": "No airplanes found"}, 404


    @staticmethod
    def create_random_airplane_tables():
        response = AirplanesDAO.create_random_airplane_tables()
        if "error" in response:
            return response, 500
        return response, 200