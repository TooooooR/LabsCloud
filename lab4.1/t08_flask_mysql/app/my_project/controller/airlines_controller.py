from flask import Blueprint, request, jsonify
from ..service.airlines_service import AirlinesService

airlines_bp = Blueprint('airlines', __name__)
airlines_bpp = Blueprint('airlines_insert', __name__)

@airlines_bpp.route('/', methods=['POST'])
def insert_dummy_airlines():
    """
    Швидке заповнення бази даних тестовими 10 записами авіакомпаній.
    ---
    tags:
        - Авіакомпанії (Airlines)
    responses:
      200:
        description: Тестові дані успішно вставлено
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Dummy airlines inserted successfully."
      500:
        description: Помилка на сервері під час вставки даних
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Database connection failed."
    """
    try:
        response = AirlinesService.insert_dummy_airlines()
        if "error" in response:
            return jsonify(response), 500
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@airlines_bp.route('/', methods=['GET'])
def get_all_airlines():
    """
            Повертає повний список усіх авіакомпаній, що зберігаються в базі даних.
            ---
            tags:
              - Авіакомпанії (Airlines)
            responses:
              200:
                description: Список авіакомпаній успішно отримано
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: Унікальний ID авіакомпанії
                      name:
                        type: string
                        description: Назва авіакомпанії
                      country:
                        type: string
                        description: Країна реєстрації
                    example:
                      - {"id": 1, "name": "Ukrainian Airlines", "country": "Ukraine"}
                      - {"id": 2, "name": "Global Air", "country": "USA"}
    """
    airlines = AirlinesService.get_all_airlines()
    return jsonify([{"id": a.id, "name": a.name, "country": a.country} for a in airlines])

@airlines_bp.route('/<int:airline_id>', methods=['GET'])
def get_airline_by_id(airline_id):
    """
        Повертає деталі конкретної авіакомпанії за її ID.
        ---
        tags:
          - Авіакомпанії (Airlines)
        parameters:
          - name: airline_id
            in: path
            type: integer
            required: true
            description: ID авіакомпанії для пошуку
        responses:
          200:
            description: Авіакомпанія знайдена
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                country:
                  type: string
            example: {"id": 1, "name": "Ukrainian Airlines", "country": "Ukraine"}
          404:
            description: Авіакомпанію не знайдено
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Airline not found"
    """
    airline = AirlinesService.get_airline_by_id(airline_id)
    if airline:
        return jsonify({"id": airline.id, "name": airline.name, "country": airline.country})
    return jsonify({"error": "Airline not found"}), 404

@airlines_bp.route('/', methods=['POST'])
def create_airline():
    """
            Створює нову авіакомпанію до бази даних.
            ---
            tags:
              - Авіакомпанії (Airlines)
            parameters:
              - name: body
                in: body
                required: true
                schema:
                  type: object
                  required:
                    - name
                    - country
                  properties:
                    name:
                      type: string
                      description: Назва авіакомпанії
                      example: 'AeroSwift'
                    country:
                      type: string
                      description: Країна реєстрації
                      example: 'Poland'
            responses:
              201:
                description: Авіакомпанія успішно створена
                schema:
                  type: object
                  properties:
                    id:
                      type: integer
                    name:
                      type: string
                    country:
                      type: string
                example: {"id": 3, "name": "AeroSwift", "country": "Poland"}
              400:
                description: Неправильний формат запиту (наприклад, відсутні поля)
    """
    data = request.get_json()
    airline = AirlinesService.create_airline(data['name'], data['country'])
    return jsonify({"id": airline.id, "name": airline.name, "country": airline.country}), 201

@airlines_bp.route('/<int:airline_id>', methods=['PUT'])
def update_airline(airline_id):
    """
            Оновлює назву та/або країну реєстрації для існуючої авіакомпанії.
            ---
            tags:
              - Авіакомпанії (Airlines)
            parameters:
              - name: airline_id
                in: path
                type: integer
                required: true
                description: ID авіакомпанії, яку потрібно оновити
              - name: body
                in: body
                required: true
                schema:
                  type: object
                  required:
                    - name
                    - country
                  properties:
                    name:
                      type: string
                      description: Нова назва авіакомпанії
                      example: 'AeroSwift International'
                    country:
                      type: string
                      description: Нова країна реєстрації
                      example: 'Germany'
            responses:
              200:
                description: Дані авіакомпанії успішно оновлено
                schema:
                  type: object
                  properties:
                    id:
                      type: integer
                    name:
                      type: string
                    country:
                      type: string
              404:
                description: Авіакомпанію не знайдено
    """
    data = request.get_json()
    airline = AirlinesService.update_airline(airline_id, data['name'], data['country'])
    if airline:
        return jsonify({"id": airline.id, "name": airline.name, "country": airline.country})
    return jsonify({"error": "Airline not found"}), 404

@airlines_bp.route('/<int:airline_id>', methods=['DELETE'])
def delete_airline(airline_id):
    """
        Видаляє запис авіакомпанії з бази даних за ID.
        ---
        tags:
          - Авіакомпанії (Airlines)
        parameters:
          - name: airline_id
            in: path
            type: integer
            required: true
            description: ID авіакомпанії, яку потрібно видалити
        responses:
          204:
            description: Авіакомпанія успішно видалена (без тіла відповіді)
          404:
            description: Авіакомпанію не знайдено
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Airline not found"
    """
    success = AirlinesService.delete_airline(airline_id)
    if success:
        return jsonify({"message": "Airline deleted"}), 204
    return jsonify({"error": "Airline not found"}), 404
