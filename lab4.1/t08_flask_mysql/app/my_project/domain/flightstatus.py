from t08_flask_mysql.app.my_project.db import db

class FlightStatus(db.Model):
    __tablename__ = 'FlightStatus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<FlightStatus {self.name}>"
