from flask import Flask, request, render_template, flash, g, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import db, Alumnos, Profesores, Pizzas, DetallePedido, Pedido, Clientes
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route('/index', methods=["GET","POST"])
def index():
    alum_form = forms.UsersForm2(request.form)
    if request.method == "POST" and alum_form.validate():
        alum = Alumnos(nombre=alum_form.nombre.data,
                        apaterno=alum_form.apaterno.data,
                        email=alum_form.email.data)
        # Insert into alumnos values()
        db.session.add(alum)
        db.session.commit()
    
    return render_template('index.html', form=alum_form)

PIZZAS = []
@app.route('/pizzeria', methods=["GET","POST"])
def pizzeria():
    cliente_form = forms.ClienteForm(request.form)
    pizza_form = forms.PizzaForm(request.form)
    dias_dict = {
        "lunes": 1,
        "martes": 2,
        "miércoles": 3,
        "jueves": 4,
        "viernes": 5,
        "sábado": 6,
        "domingo": 7
    }
    
    if request.method == "POST" and cliente_form.validate():
        nombre = cliente_form.nombre.data
        direccion = cliente_form.direccion.data
        telefono = cliente_form.telefono.data
        tamañoPizza = pizza_form.tamañoPizza.data
        jamon = request.form.get('Jamon')
        pina = request.form.get('Piña')        
        champiñones = request.form.get('Champiñones')
        numPizzas = pizza_form.numPizzas.data
        fecha = request.form.get('fecha')

        if 'agregar' in request.form and cliente_form.validate():
            pizza_data = {
                'nombre': nombre,
                'direccion': direccion,
                'telefono': telefono,
                'tamañoPizza': tamañoPizza,
                'jamon': jamon,
                'pina': pina,
                'champiñones': champiñones,
                'numPizzas': numPizzas,
                'fecha': fecha,
                'subtotal': calcular_costo_total_individual({
                    'tamañoPizza': tamañoPizza,
                    'jamon': jamon,
                    'pina': pina,
                    'champiñones': champiñones,
                    'numPizzas': numPizzas
                })
            }
            PIZZAS.append(pizza_data)
            print(PIZZAS)
            flash("La pizza se agrego")
        elif 'terminar' in request.form:
            return redirect(url_for('confirmar_pedido'))
        print(PIZZAS)
        
    if request.method == "GET" and 'buscar_ventas' in request.args:
        dia_input = request.args.get('dia')
        mes_input = request.args.get('mes')

        dia = str(dia_input).lstrip("0")
        mes = str(mes_input).lstrip("0")

        dias_semana = {
            '1': 'Lunes',
            '2': 'Martes',
            '3': 'Miércoles',
            '4': 'Jueves',
            '5': 'Viernes',
            '6': 'Sábado',
            '7': 'Domingo'
        }
        
        meses_dict = {
            '1': 'Enero',
            '2': 'Febrero',
            '3': 'Marzo',
            '4': 'Abril',
            '5': 'Mayo',
            '6': 'Junio',
            '7': 'Julio',
            '8': 'Agosto',
            '9': 'Septiembre',
            '10': 'Octubre',
            '11': 'Noviembre',
            '12': 'Diciembre'
        }
        
        dia = dias_semana.get(dia)
        mes = meses_dict.get(mes)

        query = db.session.query(Clientes.nombre, func.sum(DetallePedido.subtotal)) \
            .join(Pedido, Pedido.cliente_id == Clientes.id) \
            .join(DetallePedido, DetallePedido.pedido_id == Pedido.id) \
            .group_by(Clientes.nombre)

        if dia_input:
            if dia is not None:
                query = query.filter(Pedido.dia_semana.ilike(f'%{dia}%'))
            else:
                query = query.filter(Pedido.dia_semana.ilike(f'%{dia_input}%'))

        if mes_input:
            if mes is not None:
                query = query.filter(Pedido.mes.ilike(f'%{mes}%'))
            else:
                query = query.filter(Pedido.mes.ilike(f'%{mes_input}%'))

        ventas_acumuladas = query.all()
        print(ventas_acumuladas)

        suma_total_ventas = sum(venta[1] for venta in ventas_acumuladas)

        return render_template('pizzeria.html', form=cliente_form, pizza_form=pizza_form, ventas_acumuladas=ventas_acumuladas, suma_total=suma_total_ventas)


    if len(PIZZAS) > 0:
        cliente_form.nombre.data = PIZZAS[0]['nombre']
        cliente_form.direccion.data = PIZZAS[0]['direccion']
        cliente_form.telefono.data = PIZZAS[0]['telefono']
        
    return render_template('pizzeria.html', form=cliente_form, pizza_form = pizza_form, pizzas=PIZZAS)

@app.route('/quitar_pizza', methods=["POST"])
def quitar_pizza():
    pizza_index = int(request.form['pizza_index'])
    del PIZZAS[pizza_index]
    flash("Pizza eliminada correctamente")
    return redirect('/pizzeria')

@app.route('/confirmar_pedido', methods=["GET", "POST"])
def confirmar_pedido():
    costo_total = calcular_costo_total(PIZZAS)
    dias_semana_espanol = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }

    meses_espanol = {
        "January": "Enero",
        "February": "Febrero",
        "March": "Marzo",
        "April": "Abril",
        "May": "Mayo",
        "June": "Junio",
        "July": "Julio",
        "August": "Agosto",
        "September": "Septiembre",
        "October": "Octubre",
        "November": "Noviembre",
        "December": "Diciembre"
    }

    if request.method == "POST":
        accion = request.form.get('accion')
        if 'confirmar' == accion:
            cliente_data = PIZZAS[0]
            cliente = Clientes(
                nombre=cliente_data['nombre'],
                direccion=cliente_data['direccion'],
                telefono=cliente_data['telefono']
            )
            db.session.add(cliente)
            db.session.commit()

            fecha_str = PIZZAS[0]['fecha']
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            dia_semana = dias_semana_espanol[fecha.strftime("%A")]
            mes = meses_espanol[fecha.strftime("%B")]
            print(dia_semana)
            print(mes)

            pedido = Pedido(cliente_id=cliente.id, fecha=fecha, dia_semana=dia_semana, mes=mes)
            db.session.add(pedido)
            db.session.commit() 
            
            for pizza_data in PIZZAS:
                ing = ''
                if pizza_data['jamon']:
                    ing += 'Jamon'
                if pizza_data['pina']:
                    ing += 'Piña'
                if pizza_data['champiñones']:
                    ing += 'Champiñones'
                
                pizza = Pizzas(
                    tamanio=pizza_data['tamañoPizza'],
                    ingredientes=ing,
                    numPizzas=pizza_data['numPizzas']
                )
                db.session.add(pizza)
                db.session.commit()

                detalle_pedido = DetallePedido(
                    pedido_id=pedido.id,
                    pizza_id=pizza.id,
                    subtotal=calcular_costo_total([pizza_data])
                )
                db.session.add(detalle_pedido)

            db.session.commit()
            flash("Pedido confirmado. Gracias por tu compra.")
            
            PIZZAS.clear()
            return redirect(url_for('pizzeria'))
        elif 'editar' == accion:
            flash("Pedido cancelado.")
            return redirect(url_for('pizzeria'))

    return render_template('confirmar_pedido.html', costo_total=costo_total)


def calcular_costo_total(pizzas):
    costo_total = 0
    
    for pizza in pizzas:
        costo_pizza = 0
        
        if pizza['tamañoPizza'] == 'Chica':
            costo_pizza += 40
        elif pizza['tamañoPizza'] == 'Mediana':
            costo_pizza += 80
        elif pizza['tamañoPizza'] == 'Grande':
            costo_pizza += 120
        
        if pizza['jamon'] == 'Jamon':
            costo_pizza += 10
        if pizza['pina'] == 'Piña':
            costo_pizza += 10
        if pizza['champiñones'] == 'Champiñones':
            costo_pizza += 10
        
        costo_total += costo_pizza * pizza['numPizzas']
    
    return costo_total

def calcular_costo_total_individual(pizza):
    costo_pizza = 0
    
    if pizza['tamañoPizza'] == 'Chica':
        costo_pizza += 40
    elif pizza['tamañoPizza'] == 'Mediana':
        costo_pizza += 80
    elif pizza['tamañoPizza'] == 'Grande':
        costo_pizza += 120
    
    if pizza['jamon'] == 'Jamon':
        costo_pizza += 10
    if pizza['pina'] == 'Piña':
        costo_pizza += 10
    if pizza['champiñones'] == 'Champiñones':
        costo_pizza += 10
    
    subtotal = costo_pizza * pizza['numPizzas']
    
    return subtotal

@app.route('/ABC_Completo', methods=["GET","POST"])
def ABCompleto():
    alum_form = forms.UsersForm2(request.form)
    alumno = Alumnos.query.all()

    return render_template("/ABC_Completo.html", alumno=alumno)

@app.route('/insertarProfe', methods=["GET","POST"])
def insertar():
    profe_form = forms.ProfesorForm(request.form)
    if request.method == "POST" and profe_form.validate():
        profe = Profesores(nombre=profe_form.nombre.data,
                        apaterno=profe_form.apaterno.data,
                        materia=profe_form.materia.data,
                        edad=profe_form.edad.data)
        # Insert into profenos values()
        db.session.add(profe)
        db.session.commit()
    
    return render_template('insertarProfe.html', form=profe_form)

@app.route('/ABC_Profesor', methods=["GET","POST"])
def ABProfesor():
    profe_form = forms.ProfesorForm(request.form)
    profesor = Profesores.query.all()

    return render_template("/ABC_Profesor.html", profesor=profesor)

@app.route('/alumnos', methods=["GET","POST"])
def alumnos():
    nom = ""
    apa = ""
    ama = ""
    alum_form = forms.UserForm(request.form)
    if request.method == "POST" and alum_form.validate():
        nom = alum_form.nombre.data
        apa = alum_form.apaterno.data
        ama = alum_form.amaterno.data
        mensaje = 'Bienvenido: {}'.format(nom)
        flash(mensaje)
        print("Nombre: {}".format(nom))
        print("apaterno: {}".format(apa))
        print("amaterno: {}".format(ama))

    return render_template('alumnos.html', form = alum_form, nom = nom, apa = apa, ama = ama)

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    app.run()