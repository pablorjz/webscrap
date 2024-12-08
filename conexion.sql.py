from logging import exception
import mysql.connector
import Error
import mysql.connector
import csv

from mysql.connector import cursor


def conexion():
    try:
        ##conectamos la base de datos
        conexionDB = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="1234",
            database="cyberpuerta"
        )
        return conexionDB
    except Error as e:
        print("error al conectar en la base de datos: {e}")


##insertamos los 304 datos dentro de mysql
def insertar_datos_completos(ruta_csv):
    db = conexion()
    if db is None:
        print("no se puede establcer la conexion")
        return
    cursor = db.cursor()
    try:
        with open(ruta_csv, mode='r', encoding='utf-8-sig') as archivo:
            lector_csv = csv.reader(archivo)
            next(lector_csv)

            for fila in lector_csv:
                precio, stock, gpu, ram, rom, so, cpu, nombre = fila

                cursor.execute("INSERT IGNORE INTO sistemas_operativos (nombre) VALUES (%s)", (so,))
                cursor.execute("SELECT id FROM sistemas_operativos WHERE nombre = %s", (so,))
                id_sistema_operativo = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO  componentes (gpu,ram,rom,so,cpu)
                    VALUES (%s,%s,%s,%s,%s)
                """, (gpu, ram, rom, so, cpu))
                id_componente = cursor.lastrowid

                cursor.execute("""
                     INSERT INTO computadoras (nombre,id_componente,id_sistema_operativo)
                     VALUES (%s,%s,%s)
                """, (nombre, id_componente, id_sistema_operativo))
                id_computadora = cursor.lastrowid

                cursor.execute("INSERT INTO stock (id_computadora,cantidad) VALUES (%s,%s)", (id_computadora, stock))

                cursor.execute("INSERT INTO precios (id_computadora,precio)VALUES (%s,%s)", (id_computadora, precio))
        db.commit()
        print("datos insertados desde {ruta_csv}con exito")


    except exception as e:
        db.rollback()
        print("error al insertar datos desde el csv: {e}")

    finally:
        cursor.close()
        db.close()


def listar_computadoras():
    db = conexion()
    if db is None:
        return

    cursor = db.cursor()
    try:
        consulta = "SELECT id, nombre FROM computadoras"
        cursor.execute(consulta)
        computadoras = cursor.fetchall()

        if computadoras:
            print("computadoras disponibles")
        for computadora in computadoras:
            print(f"ID: {computadora[0]}, nombre: {computadora[1]}")
        else:
            print("no se encontraron computadoras en la base de datos")
    except Exception as e:
        print("error al listar computadoras: {e}")
    finally:
        cursor.close()
        db.close()


def insertar_stock(id_computadoras, cantidad):
    db = conexion()
    if db is None:
        print("error al conectar a la base de datos")
        return

    cursor = db.cursor()
    consulta_sql = "INSERT INTO stock (id_computadora,cantidad) VALUES (%s,%s)"
    try:
        cursor.execute(consulta_sql, (id_computadoras, cantidad))
        db.commit()
        print("stock para la computadora con ID {id_computadoras} insertado con exito")
    except Exception as e:
        db.rollback()
        print("error al insertar stock: {e}")
    finally:
        cursor.close()
        db.close()


def crear_computadoras(nombre, marca, gpu, ram, rom, cpu, sistema_operativos, precio, stock):
    db = conexion()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT IGNORE INTO marcas(nombre) VALUES (%s)", (marca,))
        cursor.execute("SELECT id FROM marcas WHERE nombre = %s", (marca,))
        id_marcas = cursor.fetchone()[0]

        cursor.execute("INSERT IGNORE INTO sistemas_operativos(nombre) VALUES (%s)", (sistema_operativos))
        cursor.execute("SELECT id FROM marcas WHERE nombre = %s", (sistema_operativos,))
        id_sistema_operativos = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO componentes (gpu,ram,rom,cpu)
            VALUES (%s,%s,%s,%s)
        """, (gpu, ram, rom, cpu))
        id_componente = cursor.lastrowid

        cursor.execute("""
            INSERT INTO computadoras (nombre,id_marca,id_componente,id_sistema_operativos)
            VALUES (%s,%s,%s,%s)
        """, (nombre, id_marcas, id_componente, sistema_operativos))
        id_computadora = cursor.lastrowid

        cursor.execute("INSERT INTO stock (id_computadora,cantidad) VALUES (%s,%s)", (id_computadora, stock))

        cursor.execute("INSERT INTO precios (id_computadora,precio)VALUES (%s,%s)", (id_computadora, precio))

        db.commit()
        print("nueva computadora'{nombre}'creada con exito")

    except Exception as e:
        db.rollback()
        print("error al crear la nueva computadora: {e}")

    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    # ruta_csv = "datasets/cyberpuerta_limpio.csv"
    # insertar_datos_completos(ruta_csv)
    """crear_computadoras(
         nombre="computadora UABC GOAT",
         marca="jordan",
         gpu="NVIDIA GeForce RTX 4090",
         ram="128",
         rom="10tb SSD",
         cpu="Intel core i7-13700k",
         sistema_operativos="Windows 11 home",
         precio=65999.99,
         stock=1
         )"""
    listar_computadoras()
    insertar_stock(305, 1)


##@erikcollado



