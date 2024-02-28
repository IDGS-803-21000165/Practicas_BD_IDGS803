from flask import Flask, render_template, request, flash, Response, g, redirect
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import db, Empleados

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/registro", methods=['GET', 'POST'])
def registro():
    emp_form = forms.Empleado(request.form)
    if request.method == 'POST':
        empleado = Empleados(
            nombre=emp_form.nombre.data,
            correo=emp_form.correo.data,
            telefono=emp_form.telefono.data,
            direccion=emp_form.direccion.data,
            sueldo=emp_form.sueldo.data)
        db.session.add(empleado)
        db.session.commit()
    return render_template("empleados.html", form=emp_form)


@app.route("/ABC_Completo", methods=['GET', 'POST'])
def ABC_Completo():
    emp_form = forms.Empleado(request.form)
    empleados = Empleados.query.all()
    return render_template("ABC_Completo.html", empleados=empleados)


@app.route("/empleados", methods=['GET', 'POST'])
def empleados():
    emp_form = forms.Empleado(request.form)
    nom = ''
    corr = ''
    tel = ''
    dirc = ''
    suel = ''
    if request.method == 'POST':
        nom = emp_form.nombre.data
        corr = emp_form.correo.data
        tel = emp_form.telefono.data
        dirc = emp_form.direccion.data
        suel = emp_form.direccion.data

    return render_template("empleados.html", form=emp_form)


if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
