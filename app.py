from flask import Flask, flash, render_template, request, redirect,url_for
from models import db, Cliente,Consumo,Facturas
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

#CRUD CLIENTES
#Crear Metodo Para Ingresar Clientes
@app.route('/clientes', methods=['GET', 'POST'])
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
    nombre = request.args.get('Nombre')
    direccion = request.args.get("Direccion")

    query = Cliente.query

    if nombre:
        query = query.filter(Cliente.Nombre.ilike(f'%{nombre}%'))
    if direccion:
        query = query.filter(Cliente.Direccion.ilike(f'%{direccion}%'))
    
    clientes = query.all()
    return render_template('Lista_Clientes.html', clientes = clientes)

#Actualizar Cliente
@app.route('/clientes/actualizar/<int:ClienteID>', methods=['GET', 'POST'])
def actualizar_Clientes(ClienteID):
    cliente = Cliente.query.get_or_404(ClienteID)

    if request.method == 'POST':
        # Asegúrate de que estos nombres coincidan con los del formulario
        cliente.Nombre = request.form.get('Nombre', cliente.Nombre)
        cliente.Direccion = request.form.get('Direccion', cliente.Direccion)
        cliente.Telefono = request.form.get('Telefono', cliente.Telefono)
        cliente.Email = request.form.get('Email', cliente.Email)

        try:
            db.session.commit()
            flash('Cliente actualizado exitosamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar cliente: {e}', 'error')
        
        return redirect(url_for('listar_Clientes'))

    return render_template('Actualizar_Cliente.html', cliente=cliente)



#Metodo para Eliminar Clientes
@app.route('/clientes/eliminar/<int:ClienteID>', methods=['POST'])
def eliminar_Cliente(ClienteID):
    cliente = Cliente.query.get_or_404(ClienteID)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('listar_Clientes'))





#Registrar Consumo de Energia Mensual
@app.route('/consumo', methods=['GET', 'POST'])
def agregar_Consumo():
    if request.method == 'POST':
        # Agregar Consumo
        ClienteID = request.form.get('ClienteID')
        Mes = request.form.get('Mes')
        Anio = request.form.get('Anio')
        Consumo_KWH = request.form.get('Consumo')

        print(f"ClienteID: {ClienteID}, Mes: {Mes}, Anio: {Anio}, Consumo_KWH: {Consumo_KWH}")
        # Validaciones
        if not ClienteID or not Mes or not Anio or not Consumo_KWH:
            flash('Todos los campos son obligatorios.', 'error')
            return redirect(url_for('agregar_Consumo'))

        try:
            # Agregar Consumo
            new_consumo = Consumo(
                ClienteID=ClienteID,
                Mes=Mes,
                Anio=Anio,
                Consumo_KWH=Consumo_KWH
            )
            db.session.add(new_consumo)
            db.session.commit()
            flash('Consumo agregado exitosamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar consumo: {e}', 'error')
        
        return redirect(url_for('agregar_Consumo'))
    
    consumos = Consumo.query.all()
    clientes = Cliente.query.all()  # Para permitir la selección de un cliente
    return render_template('Consumo.html', consumos=consumos, clientes=clientes)

@app.route("/consumo/lista")
def listar_Consumo():
    cliente_id_str = request.args.get('ClienteID')
    cliente_id = None

    if cliente_id_str:
        try:
            cliente_id = int(cliente_id_str)
        except ValueError:
            cliente_id = None

    #print(f"Filtro aplicado - ClienteID: {cliente_id}")  
    #print(f"URL de la solicitud: {request.url}")  

    query = Consumo.query

    if cliente_id is not None:
        query = query.filter_by(ClienteID=cliente_id)

    consumos = query.all()

    #print(f"Consumos encontrados: {consumos}")

    return render_template('Lista_Consumos.html', consumos=consumos, filtro_ClienteID=cliente_id)


#Crear Facturas

@app.route('/factura', methods=['GET', 'POST'])
def Factura():
    return render_template('Crear_Factura.html')


@app.route('/factura/crear_factura/<int:ClienteID>/<int:Mes>/<int:Anio>', methods=['GET', 'POST'])
def crear_factura(ClienteID, Mes, Anio):
    cliente = Cliente.query.get_or_404(ClienteID)
    consumo = Consumo.query.filter_by(ClienteID=ClienteID, Mes=Mes, Anio=Anio).first_or_404()
    
    # Calcular el total a pagar (esto es solo un ejemplo; ajusta según tu lógica de precios)
    total_a_pagar = consumo.Consumo_KWH * 0.12  # Por ejemplo, $0.12 por KWh

    if request.method == 'POST':
        try:
            # Crear la factura
            nueva_factura = Facturas(
                ClienteID=ClienteID,
                Mes=Mes,
                Anio=Anio,
                Consumo_KWH=consumo.Consumo_KWH,
                Total_Pagar=total_a_pagar,
                Fecha_Emision=datetime.now()
            )
            # Agregar la factura a la base de datos
            db.session.add(nueva_factura)
            db.session.commit()
            
            flash('Factura creada exitosamente', 'success')
            return redirect(url_for('listar_Clientes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear factura: {e}', 'error')

    return render_template('Crear_Factura.html', ClienteID=ClienteID, Mes=Mes, Anio=Anio, consumo=consumo, total_a_pagar=total_a_pagar)



    







if __name__ == '__main__':
    app.run(debug=True)