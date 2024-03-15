from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.orm import relationship

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


class Pedidos(db.Model):
    __tablename__ = 'pedido'
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(50))
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.String(10))
    fecha_compra = db.Column(db.Date)
    detalles = relationship("DetallesPedido", back_populates="pedido")


class DetallesPedido(db.Model):
    __tablename__ = 'detalle_pedido'
    id = db.Column(db.Integer, primary_key=True)
    tamanio = db.Column(db.String(50))
    ingredientes = db.Column(db.String(100))
    num_pizzas = db.Column(db.Integer)
    subtotal = db.Column(db.Float, nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    pedido = relationship("Pedidos", back_populates="detalles")
