from flask import Flask, render_template, request, flash, Response, g, redirect
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import db, Empleados, Pedidos, DetallesPedido
from sqlalchemy import text
from datetime import datetime, date

pizzas = []
total = 0
pedidos = set()

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


@app.route("/pizzeria", methods=['GET', 'POST'])
def pizzeria():
    clien_form = forms.Cliente(request.form)
    pizz_form = forms.Pizza(request.form)

    global total  # Define total como una variable global
    global pedidos  # Define pedidos como una variable global

    ventaPeriodo = 0

    if request.method == 'POST' and (pizz_form.validate() or clien_form.validate()):
        nom_com = clien_form.nombre_completo.data
        direc = clien_form.direccion.data
        tel = clien_form.telefono.data
        fecha = clien_form.fecha_compra.data

        tamanio = pizz_form.tamanio.data
        ingredientes = pizz_form.ingredientes.data
        num_pizzas = pizz_form.num_pizzas.data
        precio = 40 if pizz_form.tamanio.data == 'Chica' else (
            80 if pizz_form.tamanio.data == 'Mediana' else 120)

        nuevo_pedido = (nom_com, direc, tel, fecha)

        subtotal = (precio * num_pizzas) + ((10*len(ingredientes))*num_pizzas)
        # Ahora total es una variable global y puede ser accedida y modificada
        total = total + subtotal

        pizzas.append({'tamanio': tamanio,
                       'ingredientes': ingredientes,
                       'num_pizzas': num_pizzas,
                       'subtotal': subtotal})

        pedidos.add(nuevo_pedido)

    consulta_sql = text(f"""
            SELECT 
                p.nombre_completo AS cliente,
                SUM(dp.subtotal) AS total,
                p.fecha_compra
            FROM 
                pedido p 
            INNER JOIN 
                detalle_pedido dp ON p.id = dp.pedido_id 
            WHERE p.fecha_compra = CURDATE()
            GROUP BY p.nombre_completo, p.fecha_compra;
    """)

    ventas = db.session.execute(consulta_sql)

    for venta in ventas:
        ventaPeriodo = ventaPeriodo + venta.total

    print(ventas)
    print(ventaPeriodo)

    return render_template("pizzeria.html", form=clien_form, formp=pizz_form, pizzas=pizzas, total=total, ventas=ventas, ventaPeriodo=ventaPeriodo)


@app.route("/quitar", methods=['GET', 'POST'])
def quitar():
    global total  # Define total como una variable global
    if request.method == 'GET':
        index = int(request.args.get("index"))

        pizzaEliminada = pizzas.pop(index-1)
        total -= pizzaEliminada['subtotal']

    return redirect("pizzeria")


@app.route("/filtrarmes", methods=['GET', 'POST'])
def mes():
    ventaPeriodo = 0
    clien_form = forms.Cliente(request.form)
    pizz_form = forms.Pizza(request.form)
    consulta_sql = ''
    ventasMes = []
    ventas = []
    if request.method == 'POST':
        mes = request.form.get("mes")
        consulta_sql = text(f"""
                SELECT 
                    p.nombre_completo AS cliente,
                    SUM(dp.subtotal) AS total
                FROM 
                    pedido p 
                INNER JOIN 
                    detalle_pedido dp ON p.id = dp.pedido_id
                WHERE MONTH(p.fecha_compra) = {mes} 
                GROUP BY p.nombre_completo, MONTH(p.fecha_compra);
        """)

        ventasMes = db.session.execute(consulta_sql)
        for venta in ventasMes:
            ventas.append(venta)
            ventaPeriodo = ventaPeriodo + venta.total
    return render_template("pizzeria.html", form=clien_form, formp=pizz_form, pizzas=pizzas, total=total, ventas=ventas, ventaPeriodo=ventaPeriodo)


@app.route("/filtrarpordia", methods=['GET', 'POST'])
def dia():
    clien_form = forms.Cliente(request.form)
    pizz_form = forms.Pizza(request.form)
    consulta_sql = ''
    ventasDia = []
    ventas = []
    ventaPeriodo = 0
    print(request.form.get("dia"))
    if request.method == 'POST':
        dia = request.form.get("dia")
        print(dia)
        consulta_sql = text(f"""
                SELECT 
                    p.nombre_completo AS cliente,
                    SUM(dp.subtotal) AS total,
                    p.fecha_compra
                FROM 
                    pedido p 
                INNER JOIN 
                    detalle_pedido dp ON p.id = dp.pedido_id
                WHERE DAYNAME(fecha_compra) = '{dia}' 
                GROUP BY p.nombre_completo, p.fecha_compra;
        """)

        ventasDia = db.session.execute(consulta_sql)

        for venta in ventasDia:
            ventas.append(venta)
            ventaPeriodo = ventaPeriodo + venta.total
    return render_template("pizzeria.html", form=clien_form, formp=pizz_form, pizzas=pizzas, total=total, ventas=ventas, ventaPeriodo=ventaPeriodo)


@app.route("/modificarpedido",  methods=['GET', 'POST'])
def modificarpedido():
    pizz_form = forms.Pizza(request.form)
    global total
    if request.method == 'GET':
        index = int(request.args.get("index"))
        pizz_form.id.data = index-1
        pizz_form.tamanio.data = pizzas[index-1]['tamanio']
        pizz_form.ingredientes.data = pizzas[index-1]['ingredientes']
        pizz_form.num_pizzas.data = pizzas[index-1]['num_pizzas']
        return render_template("modificarPizza.html", formp=pizz_form)
    if request.method == 'POST':
        precio = 40 if pizz_form.tamanio.data == 'Chica' else (
            80 if pizz_form.tamanio.data == 'Mediana' else 120)

        subtotal = (precio * pizz_form.num_pizzas.data) + \
            (10*len(pizz_form.ingredientes.data))

        index = pizz_form.id.data
        total = total - pizzas[index]['subtotal']

        pizzas[index]['tamanio'] = pizz_form.tamanio.data
        pizzas[index]['ingredientes'] = pizz_form.ingredientes.data
        pizzas[index]['num_pizzas'] = pizz_form.num_pizzas.data
        pizzas[index]['subtotal'] = subtotal
        total = total + subtotal
        return redirect("pizzeria")


@app.route("/guardarpizza", methods=['GET', 'POST'])
def guardar():
    global pizzas
    global total
    global pedidos
    if request.method == 'GET':
        for pedido_actual in pedidos:
            nombre_completo, direccion, telefono, fecha_compra = pedido_actual
            pedido1 = Pedidos(nombre_completo=nombre_completo, direccion=direccion,
                              telefono=telefono, fecha_compra=fecha_compra)
            db.session.add(pedido1)
            db.session.flush()
            for pizza in pizzas:
                pizza1 = DetallesPedido(tamanio=pizza['tamanio'],
                                        ingredientes=', '.join(
                                            pizza['ingredientes']),
                                        subtotal=pizza['subtotal'],
                                        num_pizzas=pizza['num_pizzas'],
                                        pedido_id=pedido1.id)
                db.session.add(pizza1)
        db.session.commit()
    pizzas = []
    total = 0
    pedidos = set()

    return redirect("pizzeria")


if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
