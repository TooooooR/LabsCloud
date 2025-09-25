from t08_flask_mysql.app.my_project.db import db


class Airline(db.Model):
    __tablename__ = 'Airlines'  # Ім'я таблиці в нижньому регістрі

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    country = db.Column(db.String(100))

    # Визначення зв'язку для доступу до літаків, прив'язаних до авіалінії
    airplanes = db.relationship('Airplane', backref='Airline', lazy=True, cascade="all, delete-orphan")
