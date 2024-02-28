from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Empleados(db.Model):
    __tablename__ = "empleado"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    telefono = db.Column(db.String(50))
    direccion = db.Column(db.String(150))
    sueldo = db.Column(db.Float)
    fecha_registro = db.Column(db.DateTime, default=datetime.datetime.now)
