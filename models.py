from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Alumnos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apaterno = db.Column(db.String(50))
    email = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

class Profesores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apaterno = db.Column(db.String(50))
    materia = db.Column(db.String(50))
    edad = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)


class Clientes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)
    pedido = db.relationship('Pedido', backref='cliente', lazy=True)

class Pizzas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tamanio = db.Column(db.String(100))
    ingredientes = db.Column(db.String(100))
    numPizzas = db.Column(db.Integer)
 
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    fecha = db.Column(db.Date)
    dia_semana = db.Column(db.String(20))
    mes = db.Column(db.String(20))
    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True)

class DetallePedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    subtotal = db.Column(db.Float)
