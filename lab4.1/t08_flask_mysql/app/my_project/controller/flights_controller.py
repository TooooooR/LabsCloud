from flask import Blueprint, request, jsonify
from ..service.flights_service import FlightsService

flights_bp = Blueprint('flights', __name__)
flights_crew_bp = Blueprint('flights_detailed', __name__)

@flights_crew_bp.route('/', methods=['GET'])
def get_flight_crew_assignments():
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
    success = FlightsService.delete_flight(flight_id)
    if success:
        return jsonify({"message": "Flight deleted"}), 204
    return jsonify({"error": "Flight not found"}), 404
