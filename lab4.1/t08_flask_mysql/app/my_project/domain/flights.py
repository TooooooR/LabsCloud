from t08_flask_mysql.app.my_project.db import db
from t08_flask_mysql.app.my_project.domain.airports import Airport
from t08_flask_mysql.app.my_project.domain.flightstatus import FlightStatus

class Flight(db.Model):
    __tablename__ = 'Flights'

    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), unique=True, nullable=False)
    airplane_id = db.Column(db.Integer, db.ForeignKey('Airplanes.id'), nullable=False)
    departure_airport_id = db.Column(db.Integer, db.ForeignKey('Airports.id'), nullable=False)
    arrival_airport_id = db.Column(db.Integer, db.ForeignKey('Airports.id'), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('FlightStatus.id'), nullable=False)

    # Зміна імені backref, щоб уникнути конфлікту
    airplane = db.relationship('Airplane', backref='flights', lazy='joined')
    departure_airport = db.relationship('Airport', foreign_keys=[departure_airport_id], backref='outbound_flights', lazy='joined')
    arrival_airport = db.relationship('Airport', foreign_keys=[arrival_airport_id], backref='inbound_flights', lazy='joined')
    status = db.relationship('FlightStatus', backref='flights', lazy='joined')

    def __repr__(self):
        return f"<Flight {self.flight_number}>"

