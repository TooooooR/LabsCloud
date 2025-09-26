from flask import Blueprint, request, jsonify
from ..service.airlines_service import AirlinesService

airlines_bp = Blueprint('airlines', __name__)
airlines_bpp = Blueprint('airlines_insert', __name__)

@airlines_bpp.route('/', methods=['POST'])
def insert_dummy_airlines():
    try:
        response = AirlinesService.insert_dummy_airlines()
        if "error" in response:
            return jsonify(response), 500
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@airlines_bp.route('/', methods=['GET'])
def get_all_airlines():
    airlines = AirlinesService.get_all_airlines()
    return jsonify([{"id": a.id, "name": a.name, "country": a.country} for a in airlines])

@airlines_bp.route('/<int:airline_id>', methods=['GET'])
def get_airline_by_id(airline_id):
    airline = AirlinesService.get_airline_by_id(airline_id)
    if airline:
        return jsonify({"id": airline.id, "name": airline.name, "country": airline.country})
    return jsonify({"error": "Airline not found"}), 404

@airlines_bp.route('/', methods=['POST'])
def create_airline():
    data = request.get_json()
    airline = AirlinesService.create_airline(data['name'], data['country'])
    return jsonify({"id": airline.id, "name": airline.name, "country": airline.country}), 201

@airlines_bp.route('/<int:airline_id>', methods=['PUT'])
def update_airline(airline_id):
    data = request.get_json()
    airline = AirlinesService.update_airline(airline_id, data['name'], data['country'])
    if airline:
        return jsonify({"id": airline.id, "name": airline.name, "country": airline.country})
    return jsonify({"error": "Airline not found"}), 404

@airlines_bp.route('/<int:airline_id>', methods=['DELETE'])
def delete_airline(airline_id):
    success = AirlinesService.delete_airline(airline_id)
    if success:
        return jsonify({"message": "Airline deleted"}), 204
    return jsonify({"error": "Airline not found"}), 404
