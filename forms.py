from wtforms import Form
from wtforms import StringField, TextAreaField, SelectField, RadioField, IntegerField, EmailField
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
    
    
    # materias = SelectField(choices=[('Español','Esp'),('Mat','Matematicas'), ('Ingles', 'ING')])
    # radios = RadioField('Curso', choices=[("1","1"),("2","2"), ("3","3")])