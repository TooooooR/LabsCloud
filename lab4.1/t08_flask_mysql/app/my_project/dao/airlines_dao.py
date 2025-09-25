from t08_flask_mysql.app.my_project.domain.airlines import Airline
from t08_flask_mysql.app.my_project.db import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text


class AirlinesDAO:
    @staticmethod
    def get_all_airlines():
        return Airline.query.all()

    @staticmethod
    def get_airline_by_id(airline_id):
        return Airline.query.get(airline_id)

    @staticmethod
    def create_airline(name, country):
        new_airline = Airline(name=name, country=country)
        db.session.add(new_airline)
        db.session.commit()
        return new_airline

    @staticmethod
    def update_airline(airline_id, name, country):
        airline = Airline.query.get(airline_id)
        if airline:
            airline.name = name
            airline.country = country
            db.session.commit()
            return airline
        return None

    @staticmethod
    def delete_airline(airline_id):
        airline = Airline.query.get(airline_id)
        if airline:
            db.session.delete(airline)
            db.session.commit()
            return True
        return False

    @staticmethod
    def call_insert_dummy_airlines():
        try:
            db.session.execute(text("CALL insert_dummy_airlines()"))
            db.session.commit()
            return {"message": "10 dummy airlines inserted successfully"}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}
