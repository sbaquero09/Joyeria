from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:3gL9qbjeorcLUj9IQMir77maMA2wetig@dpg-cvlg438gjchc73amvdbg-a.oregon-postgres.render.com:5432/joyeria_ja8q'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Joya(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    material = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    joyas = Joya.query.all()
    return render_template('index.html', joyas=joyas)

@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('q', '')
    if query:
        joyas = Joya.query.filter(
            (Joya.nombre.contains(query)) | 
            (Joya.material.contains(query))
        ).all()
    else:
        joyas = Joya.query.all()
    return render_template('index.html', joyas=joyas)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    material = request.form['material']
    precio = float(request.form['precio'])
    stock = int(request.form['stock'])
    nueva_joya = Joya(nombre=nombre, material=material, precio=precio, stock=stock)
    db.session.add(nueva_joya)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    joya = Joya.query.get_or_404(id)
    if request.method == 'POST':
        joya.nombre = request.form['nombre']
        joya.material = request.form['material']
        joya.precio = float(request.form['precio'])
        joya.stock = int(request.form['stock'])
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', joya=joya)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    joya = Joya.query.get_or_404(id)
    db.session.delete(joya)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)