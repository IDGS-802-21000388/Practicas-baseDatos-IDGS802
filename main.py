from flask import Flask, request, render_template, flash, g
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import db, Alumnos, Profesores

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