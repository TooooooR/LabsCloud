from flask import Blueprint, request, jsonify
from ..service.airplanes_service import AirplanesService

airplanes_bp = Blueprint('airplanes', __name__)
airplanes_detailed_bp = Blueprint('airplanes_detailed', __name__)
flights_crew_bpp = Blueprint('flights_crewp', __name__)
airplanes_bpp = Blueprint('airplanes_insert', __name__)
airplanes_max = Blueprint('max_hours', __name__)
airplanes_random = Blueprint('random', __name__)

@airplanes_random.route('/', methods=['POST'])
def create_random_airplane_tables():
    try:
        response, status_code = AirplanesService.create_random_airplane_tables()
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@airplanes_max.route('/', methods=['GET'])
def get_max_flight_hours_airplane():
    """
    Повертає деталі літака, що має найбільшу загальну кількість годин польоту.
    ---
    tags:
      - Літаки (Airplanes)
    responses:
      200:
        description: Деталі літака з максимальним нальотом
        schema:
          type: object
          properties:
            id: {type: integer}
            registration_number: {type: string}
            model: {type: string}
            total_flight_hours: {type: integer}
            airline_id: {type: integer}
        example:
            id: 101
            registration_number: 'UR-FLK'
            model: 'Boeing 737'
            total_flight_hours: 15000
            airline_id: 1
      404:
        description: Жодного літака не знайдено
    """
    try:
        response, status_code = AirplanesService.get_max_flight_hours_airplane()
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@airplanes_bpp.route('/', methods=['POST'])
def insert_airplane():
    try:
        data = request.get_json()
        registration_number = data.get('registration_number')
        model = data.get('model')
        total_flight_hours = data.get('total_flight_hours')
        airline_id = data.get('airline_id')

        if not all([registration_number, model, total_flight_hours, airline_id]):
            return jsonify({"error": "All fields are required"}), 400

        response = AirplanesService.insert_airplane(
            registration_number, model, total_flight_hours, airline_id
        )
        if isinstance(response, dict):
            # Повертаємо структуру відповіді JSON із статусом
            return jsonify(response), response.get("status", 200)
        return jsonify({"error": "Unexpected response format"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@flights_crew_bpp.route('/', methods=['POST'])
def insert_flight_crew():
    """
    Створює запис про призначення екіпажу до конкретного рейсу.
    ---
    tags:
      - Літаки (Airplanes)
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required: [flight_number, crew_name]
          properties:
            flight_number: {type: string, description: Номер рейсу, наприклад, 'PS123', example: 'KL456'}
            crew_name: {type: string, description: Ім'я члена екіпажу, example: 'Іван Коваленко'}
    responses:
      200:
        description: Екіпаж успішно призначено
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Flight KL456 crew set for Іван Коваленко"
      400:
        description: Неправильні дані або помилка призначення
    """
    data = request.get_json()
    result = AirplanesService.insert_flight_crew(
        data['flight_number'],
        data['crew_name']
    )
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 200

@airplanes_detailed_bp.route('/', methods=['GET'])
def get_all_airplanes_detailed():
    """
    Повертає повний список літаків із додатковою інформацією.
    ---
    tags:
      - Літаки (Airplanes)
    responses:
      200:
        description: Детальний список літаків
        schema:
          type: array
          items:
            type: object
            properties:
              id: {type: integer}
              model: {type: string}
              airline_name: {type: string, description: Назва авіакомпанії}
              total_flight_hours: {type: integer}
              # ... інші деталі
    """
    airplanes_detailed = AirplanesService.get_all_airplanes_detailed()
    return jsonify(airplanes_detailed)

@airplanes_bp.route('/', methods=['GET'])
def get_all_airplanes():
    """
        Повертає базовий список усіх літаків.
        ---
        tags:
          - Літаки (Airplanes)
        responses:
          200:
            description: Базовий список літаків
            schema:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  registration_number: {type: string}
                  model: {type: string}
                  total_flight_hours: {type: integer}
                  airline_id: {type: integer}
    """
    airplanes = AirplanesService.get_all_airplanes()
    return jsonify([
        {
            "id": a.id,
            "registration_number": a.registration_number,
            "model": a.model,
            "total_flight_hours": a.total_flight_hours,
            "airline_id": a.airline_id
        } for a in airplanes
    ])

@airplanes_bp.route('/<int:airplane_id>', methods=['GET'])
def get_airplane_by_id(airplane_id):
    """
    Повертає деталі конкретного літака за його ID.
    ---
    tags:
      - Літаки (Airplanes)
    parameters:
      - name: airplane_id
        in: path
        type: integer
        required: true
        description: ID літака для пошуку
    responses:
      200:
        description: Літак знайдено
        schema:
          type: object
          properties:
            id: {type: integer}
            registration_number: {type: string}
            model: {type: string}
            total_flight_hours: {type: integer}
            airline_id: {type: integer}
      404:
        description: Літак не знайдено
    """
    airplane = AirplanesService.get_airplane_by_id(airplane_id)
    if airplane:
        return jsonify({
            "id": airplane.id,
            "registration_number": airplane.registration_number,
            "model": airplane.model,
            "total_flight_hours": airplane.total_flight_hours,
            "airline_id": airplane.airline_id
        })
    return jsonify({"error": "Airplane not found"}), 404

@airplanes_bp.route('/', methods=['POST'])
def create_airplane():
    """
        Створити новий літак в базі даних.
        ---
        tags:
          - Літаки (Airplanes)
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required: [registration_number, model, total_flight_hours, airline_id]
              properties:
                registration_number: {type: string, example: 'UR-JKL'}
                model: {type: string, example: 'Boeing 737'}
                total_flight_hours: {type: integer, example: 100}
                airline_id: {type: integer, example: 1}
        responses:
          201:
            description: Літак успішно створений
            schema:
              type: object
              properties:
                id: {type: integer}
                registration_number: {type: string}
                model: {type: string}
                total_flight_hours: {type: integer}
                airline_id: {type: integer}
          400:
            description: Неправильний формат запиту
    """
    data = request.get_json()
    airplane = AirplanesService.create_airplane(
        data['registration_number'],
        data['model'],
        data['total_flight_hours'],
        data['airline_id']
    )
    return jsonify({
        "id": airplane.id,
        "registration_number": airplane.registration_number,
        "model": airplane.model,
        "total_flight_hours": airplane.total_flight_hours,
        "airline_id": airplane.airline_id
    }), 201

@airplanes_bp.route('/<int:airplane_id>', methods=['PUT'])
def update_airplane(airplane_id):
    """
        Оновлює деталі існуючого літака за ID.
        ---
        tags:
          - Літаки (Airplanes)
        parameters:
          - name: airplane_id
            in: path
            type: integer
            required: true
            description: ID літака, який потрібно оновити
          - name: body
            in: body
            required: true
            schema:
              type: object
              required: [registration_number, model, total_flight_hours, airline_id]
              properties:
                registration_number: {type: string, example: 'UR-JKL'}
                model: {type: string, example: 'Boeing 737 MAX'}
                total_flight_hours: {type: integer, example: 150}
                airline_id: {type: integer, example: 1}
        responses:
          200:
            description: Дані літака успішно оновлено
            schema:
              type: object
              properties:
                id: {type: integer}
                registration_number: {type: string}
                model: {type: string}
                total_flight_hours: {type: integer}
                airline_id: {type: integer}
          404:
            description: Літак не знайдено
    """
    data = request.get_json()
    airplane = AirplanesService.update_airplane(
        airplane_id,
        data['registration_number'],
        data['model'],
        data['total_flight_hours'],
        data['airline_id']
    )
    if airplane:
        return jsonify({
            "id": airplane.id,
            "registration_number": airplane.registration_number,
            "model": airplane.model,
            "total_flight_hours": airplane.total_flight_hours,
            "airline_id": airplane.airline_id
        })
    return jsonify({"error": "Airplane not found"}), 404

@airplanes_bp.route('/<int:airplane_id>', methods=['DELETE'])
def delete_airplane(airplane_id):
    """
        Видаляє запис літака з бази даних.
        ---
        tags:
          - Літаки (Airplanes)
        parameters:
          - name: airplane_id
            in: path
            type: integer
            required: true
            description: ID літака, який потрібно видалити
        responses:
          204:
            description: Літак успішно видалено (без тіла відповіді)
          404:
            description: Літак не знайдено
    """
    success = AirplanesService.delete_airplane(airplane_id)
    if success:
        return jsonify({"message": "Airplane deleted"}), 204
    return jsonify({"error": "Airplane not found"}), 404


