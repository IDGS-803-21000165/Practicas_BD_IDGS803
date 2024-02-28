from wtforms import Form
from wtforms import StringField, EmailField, IntegerField, FloatField
from wtforms import validators


class Empleado(Form):
    id = IntegerField('id')
    nombre = StringField("Nombre", [
        validators.DataRequired(message='El campo nombre es requerido'),
        validators.length(min=4, max=50, message='Ingrese nombre valido')])

    correo = EmailField("Correo", [
        validators.Email(message='Ingrese un correo valido')
    ])

    telefono = StringField("Telefono", [
        validators.DataRequired(message='El campo telefono es requerido'),
        validators.length(min=4, max=10, message='Ingrese telefono valido')])

    direccion = StringField("Dirección", [
        validators.DataRequired(message='El campo direccion es requerido'),
        validators.length(min=4, max=150, message='Ingrese una direccion valida')])

    sueldo = FloatField("Sueldo", [
        validators.DataRequired(message='El campo sueldo es requerido'),
        validators.length(min=4, max=10, message='Ingrese sueldo valido')])
