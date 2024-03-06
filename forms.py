from wtforms import Form
from wtforms import StringField, BooleanField, RadioField, IntegerField, EmailField
from wtforms import validators


class UserForm(Form):    
    nombre = StringField("nombre",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message='Ingrese nombre valido')
    ])
    apaterno =StringField("apaterno")
    amaterno = StringField("amaterno")
    edad = IntegerField('edad',
        [validators.number_range(min=1, max=20, message='Valor no valido')])
    correo = EmailField("correo",
        [validators.Email(message='Ingrese un correo valido')])
    
class UsersForm2(Form):
    id = IntegerField("id")
    nombre = StringField("nombre",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message='Ingrese nombre valido')
    ])
    apaterno =StringField("apaterno")
    email = EmailField("correo",[
        validators.Email(message='Ingrese un correo valido')
    ])
    
class ProfesorForm(Form):
    id = IntegerField("id")
    nombre = StringField("nombre",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message='Ingrese nombre valido')
    ])
    apaterno =StringField("apaterno")
    materia =StringField("materia")
    edad =StringField("edad")

class PizzaForm(Form):
    tamañoPizza = RadioField('Tamaño Pizza', choices=[("Chica","Chica 40$"),("Mediana","Mediana 80$"),("Grande","Grande 120$")])
    numPizzas = IntegerField('Número de pizzas', validators=[validators.number_range(min=1, max=20, message='Valor no válido')])

class ClienteForm(Form):
    nombre = StringField("Nombre", validators=[validators.DataRequired(message='El campo es requerido')])
    direccion = StringField("Dirección", validators=[validators.DataRequired(message='El campo es requerido')])
    telefono = StringField("Teléfono", validators=[validators.DataRequired(message='El campo es requerido')])

# class PizzeriaForm(Form):
#     id = IntegerField("id")
#     nombre = StringField("nombre",[
#         validators.DataRequired(message='El campo es requerido'),
#         validators.length(min=4, max=10, message='Ingrese nombre valido')
#     ])
#     direccion = StringField("direccion",[
#         validators.DataRequired(message='El campo es requerido'),
#         validators.length(min=4, max=10, message='Ingrese nombre valido')
#     ])
#     telefono = StringField("telefono",[
#         validators.DataRequired(message='El campo es requerido'),
#         validators.length(min=4, max=10, message='Ingrese nombre valido')
#     ])
#     tamañoPizza = RadioField('Tamaño Pizza', choices=[("Chica","Chica 40$"),("Mediana","Mediana 80$"),("Grande","Grande 120$")])
#     numPizzas = IntegerField('numero de pizzas',
#         [validators.number_range(min=1, max=20, message='Valor no valido')])

    
    
    # materias = SelectField(choices=[('Español','Esp'),('Mat','Matematicas'), ('Ingles', 'ING')])
    # radios = RadioField('Curso', choices=[("1","1"),("2","2"), ("3","3")])