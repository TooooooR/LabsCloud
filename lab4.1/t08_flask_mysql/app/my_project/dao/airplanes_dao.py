from ..db import db
from ..domain.airplanes import Airplane
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

class AirplanesDAO:
    @staticmethod
    def get_all_airplanes():
        return Airplane.query.all()

    @staticmethod
    def get_airplane_by_id(airplane_id):
        return Airplane.query.get(airplane_id)

    @staticmethod
    def create_airplane(registration_number, model, total_flight_hours, airline_id):
        new_airplane = Airplane(
            registration_number=registration_number,
            model=model,
            total_flight_hours=total_flight_hours,
            airline_id=airline_id
        )
        db.session.add(new_airplane)
        db.session.commit()
        return new_airplane

    @staticmethod
    def update_airplane(airplane_id, registration_number, model, total_flight_hours, airline_id):
        airplane = Airplane.query.get(airplane_id)
        if airplane:
            airplane.registration_number = registration_number
            airplane.model = model
            airplane.total_flight_hours = total_flight_hours
            airplane.airline_id = airline_id
            db.session.commit()
        return airplane

    @staticmethod
    def delete_airplane(airplane_id):
        airplane = Airplane.query.get(airplane_id)
        if airplane:
            db.session.delete(airplane)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_all_airplanes_detailed():
        airplanes = Airplane.query.all()  # Отримуємо всі літаки разом із їх зв'язаними авіакомпаніями через relationship
        return [
            {
                "id": airplane.id,
                "registration_number": airplane.registration_number,
                "model": airplane.model,
                "total_flight_hours": airplane.total_flight_hours,
                "airline": {
                    "id": airplane.airline.id,
                    "name": airplane.airline.name,
                    "country": airplane.airline.country
                }
            } for airplane in airplanes
        ]

    @staticmethod
    def call_insert_airplane(registration_number, model, total_flight_hours, airline_id):
        try:
            db.session.execute(
                text("""
                CALL insert_airplane(:registration_number, :model, :total_flight_hours, :airline_id)
                """),
                {
                    'registration_number': registration_number,
                    'model': model,
                    'total_flight_hours': total_flight_hours,
                    'airline_id': airline_id
                }
            )
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            return str(e)

    @staticmethod
    def get_max_flight_hours_airplane():
        try:
            result = db.session.execute(text("CALL get_max_flight_hours_airplane_proc()"))
            airplane_data = result.fetchall()
            return airplane_data
        except SQLAlchemyError as e:
            return {"error": str(e)}

    @staticmethod
    def create_random_airplane_tables():
        try:
            db.session.execute(text("CALL create_random_airplane_tables()"))
            db.session.commit()
            return {"message": "Random airplane tables created successfully"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}