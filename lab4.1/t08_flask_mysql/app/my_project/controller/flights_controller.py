from flask import Blueprint, request, jsonify
from ..service.flights_service import FlightsService

flights_bp = Blueprint('flights', __name__)
flights_crew_bp = Blueprint('flights_detailed', __name__)

@flights_crew_bp.route('/', methods=['GET'])
def get_flight_crew_assignments():
    """
        Повертає повний список призначень членів екіпажу до конкретних рейсів.
        ---
        tags:
          - Рейси (Flights)
        responses:
          200:
            description: Список призначень екіпажів успішно отримано
            schema:
              type: array
              items:
                type: object
                properties:
                  flight_id: {type: integer, description: ID рейсу}
                  flight_number: {type: string, description: Номер рейсу}
                  crew_id: {type: integer, description: ID члена екіпажу}
                  crew_member_name: {type: string, description: Ім'я члена екіпажу}
                  crew_member_position: {type: string, description: Посада}
                example: [{"flight_id": 1, "flight_number": "PS101", "crew_id": 5, "crew_member_name": "Олена Петрова", "crew_member_position": "Капітан"}]
    """
    assignments = FlightsService.get_flight_crew_assignments()
    return jsonify([{
        "flight_id": a.flight_id,
        "flight_number": a.flight_number,
        "crew_id": a.crew_id,
        "crew_member_name": a.crew_member_name,
        "crew_member_position": a.crew_member_position
    } for a in assignments])

@flights_bp.route('/', methods=['GET'])
def get_all_flights():
    """
            Повертає базовий список усіх рейсів, зареєстрованих у системі.
            ---
            tags:
              - Рейси (Flights)
            responses:
              200:
                description: Список рейсів успішно отримано
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      id: {type: integer}
                      flight_number: {type: string}
                      airplane_id: {type: integer, description: ID літака}
                      departure_airport_id: {type: integer, description: ID аеропорту вильоту}
                      arrival_airport_id: {type: integer, description: ID аеропорту прибуття}
                      departure_time: {type: string, format: date-time}
                      arrival_time: {type: string, format: date-time}
                      status_id: {type: integer, description: ID статусу рейсу}
    """
    flights = FlightsService.get_all_flights()
    return jsonify([{
        "id": f.id,
        "flight_number": f.flight_number,
        "airplane_id": f.airplane_id,
        "departure_airport_id": f.departure_airport_id,
        "arrival_airport_id": f.arrival_airport_id,
        "departure_time": f.departure_time,
        "arrival_time": f.arrival_time,
        "status_id": f.status_id
    } for f in flights])

@flights_bp.route('/<int:flight_id>', methods=['GET'])
def get_flight_by_id(flight_id):
    """
            Отримати рейс за ID.
            ---
            tags:
              - Рейси (Flights)
            parameters:
              - name: flight_id
                in: path
                type: integer
                required: true
                description: ID рейсу для пошуку
            responses:
              200:
                description: Рейс знайдено
                schema:
                  type: object
                  properties:
                    id: {type: integer}
                    flight_number: {type: string}
                    airplane_id: {type: integer}
                    departure_airport_id: {type: integer}
                    arrival_airport_id: {type: integer}
                    departure_time: {type: string, format: date-time}
                    arrival_time: {type: string, format: date-time}
                    status_id: {type: integer}
              404:
                description: Рейс не знайдено
    """
    flight = FlightsService.get_flight_by_id(flight_id)
    if flight:
        return jsonify({
            "id": flight.id,
            "flight_number": flight.flight_number,
            "airplane_id": flight.airplane_id,
            "departure_airport_id": flight.departure_airport_id,
            "arrival_airport_id": flight.arrival_airport_id,
            "departure_time": flight.departure_time,
            "arrival_time": flight.arrival_time,
            "status_id": flight.status_id
        })
    return jsonify({"error": "Flight not found"}), 404

@flights_bp.route('/', methods=['POST'])
def create_flight():
    """
        Створює новий запис рейсу з усіма необхідними деталями.
        ---
        tags:
          - Рейси (Flights)
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required: [flight_number, airplane_id, departure_airport_id, arrival_airport_id, departure_time, arrival_time, status_id]
              properties:
                airplane_id: {type: integer, example: 1}
                arrival_airport_id: {type: integer, example: 3}
                departure_airport_id: {type: integer, example: 5}
                flight_number: {type: string, example: 'UA999'}
                status_id: {type: integer, example: 2, description: Новий ID статусу (наприклад, Вилетів)}
                departure_time: {type: string, format: date-time, example: "2025-09-15 14:00:00"}
                arrival_time: {type: string, format: date-time, example: "2025-09-16 15:00:00"}
        responses:
          201:
            description: Рейс успішно створений
          400:
            description: Неправильний формат запиту
    """
    data = request.get_json()
    flight = FlightsService.create_flight(data)
    return jsonify({
        "id": flight.id,
        "flight_number": flight.flight_number,
        "airplane_id": flight.airplane_id,
        "departure_airport_id": flight.departure_airport_id,
        "arrival_airport_id": flight.arrival_airport_id,
        "departure_time": flight.departure_time,
        "arrival_time": flight.arrival_time,
        "status_id": flight.status_id
    }), 201

@flights_bp.route('/<int:flight_id>', methods=['PUT'])
def update_flight(flight_id):
    """
        Оновлює деталі існуючого рейсу за ID.
        ---
        tags:
          - Рейси (Flights)
        parameters:
          - name: flight_id
            in: path
            type: integer
            required: true
            description: ID рейсу, який потрібно оновити
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                airplane_id: {type: integer, example: 1}
                arrival_airport_id: {type: integer, example: 3}
                departure_airport_id: {type: integer, example: 5}
                flight_number: {type: string, example: 'UA999'}
                status_id: {type: integer, example: 2, description: Новий ID статусу (наприклад, Вилетів)}
        responses:
          200:
            description: Дані рейсу успішно оновлено
          404:
            description: Рейс не знайдено
    """
    data = request.get_json()
    flight = FlightsService.update_flight(flight_id, data)
    if flight:
        return jsonify({
            "id": flight.id,
            "flight_number": flight.flight_number,
            "airplane_id": flight.airplane_id,
            "departure_airport_id": flight.departure_airport_id,
            "arrival_airport_id": flight.arrival_airport_id,
            "departure_time": flight.departure_time,
            "arrival_time": flight.arrival_time,
            "status_id": flight.status_id
        })
    return jsonify({"error": "Flight not found"}), 404

@flights_bp.route('/<int:flight_id>', methods=['DELETE'])
def delete_flight(flight_id):
    """
        Видаляє запис рейсу з бази даних.
        ---
        tags:
          - Рейси (Flights)
        parameters:
          - name: flight_id
            in: path
            type: integer
            required: true
            description: ID рейсу, який потрібно видалити
        responses:
          204:
            description: Рейс успішно видалено (без тіла відповіді)
          404:
            description: Рейс не знайдено
    """
    success = FlightsService.delete_flight(flight_id)
    if success:
        return jsonify({"message": "Flight deleted"}), 204
    return jsonify({"error": "Flight not found"}), 404
