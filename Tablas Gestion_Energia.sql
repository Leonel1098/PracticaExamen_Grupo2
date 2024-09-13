create database Gestion_Energia

use Gestion_Energia

Create Table Cliente
(
ClienteId INT Primary Key IDENTITY(1,1),
Nombre VARCHAR (100) NOT NULL,
Direccion VARCHAR(200) NOT NULL,
Telefono VARCHAR(15) NOT NULL,
Email VARCHAR (100) NOT NULL);


Create table Consumo
(
ConsumoId INT Primary Key IDENTITY(1,1),
ClienteId INT NOT NULL,
Mes VARCHAR (20) NOT NULL,
Anio INT NOT NULL,
Consumo_KWH FLOAT NOT NULL,
constraint fk_ConsumoCliente foreign key (ClienteId) References Cliente(ClienteId));

Create table Facturas
(
FacturaId INT Primary Key IDENTITY(1,1),
ClienteId INT NOT NULL,
Fecha_Emision DATE NOT NULL,
Monto_Total FLOAT NOT NULL,
Estado BIT NOT NULL DEFAULT 1,
constraint fk_FacturaCliente foreign key (ClienteID) References Cliente(ClienteID));




delete Cliente
select * from Cliente
select * from Consumo
select * from Facturas