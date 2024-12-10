create database if not exists Cyberpuerta;
use Cyberpuerta;

CREATE TABLE marcas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE sistemas_operativos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE componentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gpu VARCHAR(255),
    ram VARCHAR(255),
    rom VARCHAR(255),
    cpu VARCHAR(255)
);

CREATE TABLE computadoras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    id_marca INT,
    id_componentes INT,
    id_sistema_operativo INT,
    FOREIGN KEY (id_marca) REFERENCES marcas(id),
    FOREIGN KEY (id_componentes) REFERENCES componentes(id),
    FOREIGN KEY (id_sistema_operativo) REFERENCES sistemas_operativos(id)
);

CREATE TABLE stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_computadora INT,
    cantidad INT NOT NULL,
    FOREIGN KEY (id_computadora) REFERENCES computadoras(id)
);

CREATE TABLE precios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_computadora INT,
    precio DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_computadora) REFERENCES computadoras(id)
);

select id, nombre from computadoras;