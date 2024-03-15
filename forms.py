from wtforms import Form
from wtforms import StringField, EmailField, IntegerField, FloatField, DateField, RadioField, TelField, SelectMultipleField, widgets
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


class CheckboxSelectMultipleField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Pizza(Form):
    OPCIONES_TAMANIO = [
        ('Chica', 'Chica - $40'),
        ('Mediana', 'Mediana - $80'),
        ('Grande', 'Grande - $120')
    ]

    OPCIONES_INGREDIENTES = [
        ('Jamon', 'Jamon - $10'),
        ('Piña', 'Piña - $10'),
        ('Champiñones', 'Champiñones - $10')
    ]

    id = IntegerField('id')

    tamanio = RadioField("Tamaño", choices=OPCIONES_TAMANIO)

    ingredientes = CheckboxSelectMultipleField(
        'Ingredientes: ', choices=OPCIONES_INGREDIENTES)

    num_pizzas = IntegerField("Número de pizzas", [
        validators.DataRequired(
            message='El campo número de pizzas es requerido'),
        validators.number_range(min=1, max=20, message='valor no valido')])


class Cliente(Form):
    id = IntegerField("id")

    nombre_completo = StringField("Nombre Completo", [
        validators.DataRequired(message='El campo nombre es requerido'),
        validators.length(min=4, max=150, message='Ingrese un nombre valido')])

    direccion = StringField("Dirección", [
        validators.DataRequired(message='El campo direccion es requerido'),
        validators.length(min=4, max=150, message='Ingrese una direccion valida')])

    telefono = TelField("Teléfono", [
        validators.DataRequired(message='El campo teléfono es requerido'),
        validators.length(min=4, max=10, message='Ingrese un teléfono valido')])

    fecha_compra = DateField("Fecha de compra", [
        validators.DataRequired(message='El campo fecha es requerido')])
