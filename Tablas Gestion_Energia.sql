create database Gestion_Energia

use Gestion_Energia

Create Table Cliente
(
clienteid INT Primary Key,
nombre VARCHAR (100),
direccion VARCHAR(200),
telefono VARCHAR(15),
email VARCHAR (100));


Create table Consumo
(
consumoid INT Primary Key,
clienteid INT,
mes VARCHAR (20),
anio INT,
consumo_kwh FLOAT,
constraint fk_ConsumoCliente foreign key (clienteid)
References Cliente(clienteid));

Create table Facturas
(
facturaid INT Primary Key,
clienteid INT,
fecha_emision DATE,
monto_total FLOAT,
estado bit,

constraint fk_FacturaCliente foreign key (clienteid)
References Cliente(clienteid));
