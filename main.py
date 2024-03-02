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


@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    emp_form = forms.Empleado(request.form)
    if request.method == 'GET':
        id = request.args.get("id")
        emp1 = db.session.query(Empleados).filter(
            Empleados.id == id).first()
        emp_form.id.data = request.args.get('id')
        emp_form.nombre.data = emp1.nombre
        emp_form.correo.data = emp1.correo
        emp_form.telefono.data = emp1.telefono
        emp_form.direccion.data = emp1.direccion
        emp_form.sueldo.data = emp1.sueldo
    if request.method == 'POST':
        id = emp_form.id.data
        empleado = Empleados.query.get(id)
        db.session.delete(empleado)
        db.session.commit()
        return redirect("ABC_Completo")

    return render_template("eliminar.html", form=emp_form)


@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    emp_form = forms.Empleado(request.form)
    if request.method == 'GET':
        id = request.args.get("id")
        emp1 = db.session.query(Empleados).filter(
            Empleados.id == id).first()
        emp_form.id.data = request.args.get('id')
        emp_form.nombre.data = emp1.nombre
        emp_form.correo.data = emp1.correo
        emp_form.telefono.data = emp1.telefono
        emp_form.direccion.data = emp1.direccion
        emp_form.sueldo.data = emp1.sueldo
    if request.method == 'POST':
        id = emp_form.id.data
        empleado = db.session.query(Empleados).filter(
            Empleados.id == id).first()
        empleado.nombre = emp_form.nombre.data
        empleado.correo = emp_form.correo.data
        empleado.telefono = emp_form.telefono.data
        empleado.direccion = emp_form.direccion.data
        empleado.sueldo = emp_form.sueldo.data
        db.session.add(empleado)
        db.session.commit()
        return redirect("ABC_Completo")

    return render_template("modificar.html", form=emp_form)


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
