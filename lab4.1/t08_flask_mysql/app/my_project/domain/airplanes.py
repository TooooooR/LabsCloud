from ..db import db

class Airplane(db.Model):
    __tablename__ = 'Airplanes'  # Ім'я таблиці має бути в нижньому регістрі для відповідності з ForeignKey

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100))
    registration_number = db.Column(db.String(100))
    total_flight_hours = db.Column(db.Integer)
    airline_id = db.Column(db.Integer, db.ForeignKey('Airlines.id'))  # Збігається з __tablename__ моделі Airline

    airline = db.relationship('Airline', back_populates='airplanes')

    def __repr__(self):
        return f"<Airplane {self.registration_number}>"
