import datetime
from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Configurando la base de Datos 
app.config["SQLALCHEMY_DATABASE_URI"] = 'mssql+pyodbc://Leonel:Leonel@PC-DEV14/Gestion_Energia?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cliente(db.Model):
    __tablename__ = 'Cliente'
    ClienteID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Direccion = db.Column(db.String(200), nullable=False)
    Telefono = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    consumo = db.relationship('Consumo', backref='cliente', lazy=True)
    factura = db.relationship("Facturas", backref = "factura", lazy = True)

class Consumo(db.Model):
    __tablename__ = 'Consumo'
    ConsumoID = db.Column(db.Integer, primary_key=True)
    ClienteID = db.Column(db.Integer, db.ForeignKey('Cliente.ClienteID'), nullable=False)
    Mes = db.Column(db.String(50), unique=True, nullable=False)
    Año = db.Column(db.Integer, unique=True, nullable=False)
    Consumo_KWH = db.Column(db.Float, nullable=False)

class Facturas(db.Model):
    __tablename__ = 'Facturas'
    FacturaID = db.Column(db.Integer, primary_key=True)
    ClienteID = db.Column(db.Integer, db.ForeignKey('Cliente.ClienteID'), nullable=False)
    Fecha_Emision = db.Column(db.DateTime, nullable=False)
    Estado = db.Column(db.Boolean, default=True, nullable=False)

@app.route("/")
def index():
    return render_template("index.html")

#Crear Metodo Para Ingresar Clientes
@app.route('/vehiculos', methods=['GET', 'POST'])
def crear_Cliente():
    if request.method == 'POST':
        # Crear nuevo cliente
        new_cliente = Cliente(
            Nombre=request.form['Nombre'],
            Direccion=request.form['Direccion'],
            Telefono=request.form['Telefono'],
            Email=request.form['Email'],
        )
        db.session.add(new_cliente)
        db.session.commit()
        return redirect(url_for('listar_Clientes'))
    
    clientes = Cliente.query.all()
    return render_template('Clientes.html', clientes = clientes)


#Crear Metodo Para Listar Clientes
@app.route("/clientes/lista")
def listar_Clientes():
    clientes = Cliente.query.all()
    return render_template('Lista_Clientes.html', clientes = clientes)

#Registrar Consumo de Energia Mensual
@app.route('/consumo', methods=['GET', 'POST'])
def agregar_Consumo():
    if request.method == 'POST':
        # Agregar Consumo
        new_consumo = Consumo(
            ClienteID=request.form['ClienteID'],
            Año=request.form['Año'],
            Consumo=request.form['Consumo'],
        )
        db.session.add(new_consumo)
        db.session.commit()
        return redirect(url_for('listar_Consumos'))
    
    consumo = Consumo.query.all()
    return render_template('Consumo.html', consumo = consumo)



if __name__ == '__main__':
    app.run(debug=True)