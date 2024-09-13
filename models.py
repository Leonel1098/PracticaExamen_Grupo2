from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'Cliente'
    ClienteID = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Direccion = db.Column(db.String(200), nullable=False)
    Telefono = db.Column(db.String(15), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    
    # Relación con la tabla Consumo
    consumos = db.relationship('Consumo', backref='cliente', lazy=True)
    
    # Relación con la tabla Facturas
    facturas = db.relationship('Facturas', backref='cliente', lazy=True)

class Consumo(db.Model):
    __tablename__ = 'Consumo'
    ConsumoID = db.Column(db.Integer, primary_key=True)
    ClienteID = db.Column(db.Integer, db.ForeignKey('Cliente.ClienteID'), nullable=False)
    Mes = db.Column(db.String(20), nullable=False)  
    Anio = db.Column(db.Integer, nullable=False)
    Consumo_KWH = db.Column(db.Float, nullable=False)

class Facturas(db.Model):
    __tablename__ = 'Facturas'
    FacturaID = db.Column(db.Integer, primary_key=True)
    ClienteID = db.Column(db.Integer, db.ForeignKey('Cliente.ClienteID'), nullable=False)
    Fecha_Emision = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Monto_Total = db.Column(db.Float, nullable=False)  
    Estado = db.Column(db.Boolean, default=True, nullable=False)
