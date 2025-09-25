from t08_flask_mysql.app.my_project.dao.airlines_dao import AirlinesDAO


class AirlinesService:
    @staticmethod
    def get_all_airlines():
        return AirlinesDAO.get_all_airlines()

    @staticmethod
    def get_airline_by_id(airline_id):
        return AirlinesDAO.get_airline_by_id(airline_id)

    @staticmethod
    def create_airline(name, country):
        return AirlinesDAO.create_airline(name, country)

    @staticmethod
    def update_airline(airline_id, name, country):
        return AirlinesDAO.update_airline(airline_id, name, country)

    @staticmethod
    def delete_airline(airline_id):
        return AirlinesDAO.delete_airline(airline_id)

    @staticmethod
    def insert_dummy_airlines():
        return AirlinesDAO.call_insert_dummy_airlines()
