from ..db import db

class Airport(db.Model):
    __tablename__ = 'Airports'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)

    # Відношення до рейсів
    departing_flights = db.relationship(
        'Flight',
        foreign_keys='Flight.departure_airport_id',
        back_populates='departure_airport',  # Використовуємо back_populates
        lazy=True,
        cascade="all, delete-orphan"
    )
    arriving_flights = db.relationship(
        'Flight',
        foreign_keys='Flight.arrival_airport_id',
        back_populates='arrival_airport',  # Використовуємо back_populates
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Airport {self.code}>"
