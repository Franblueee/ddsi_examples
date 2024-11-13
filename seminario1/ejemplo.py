import psycopg2 as pg

# Conectarse a la base de datos
conn = pg.connect(
    database='banco',
    user='fran',
    password='fran',
    host='localhost',
)
conn.autocommit = False

id_origen = input('Ingrese el identificador de la cuenta de la que desea sacar dinero: ')
id_destino = input('Ingrese el identificador de la cuenta a la que desea ingresar dinero: ')
cantidad = input('Ingrese la cantidad de dinero que desea sacar: ')
cantidad = float(cantidad)

# Crear un cursor
cur = conn.cursor()

# Crear checkpoint
cur.execute("BEGIN;")
cur.execute("SAVEPOINT s1;")

# Comprobar que las cuentas existen
try:
    cur.execute(f"SELECT idcuenta FROM cuenta WHERE idcuenta = {id_origen} FOR UPDATE;")
    data = cur.fetchall()
    if len(data) == 0:
        raise Exception("La cuenta de origen no existe")
    cur.execute(f"SELECT idcuenta FROM cuenta WHERE idcuenta = {id_destino} FOR UPDATE;")
    data = cur.fetchall()
    if len(data) == 0:
        raise Exception("La cuenta de destino no existe")
except Exception as e:
    cur.execute("ROLLBACK TO SAVEPOINT s1;")
    cur.execute("RELEASE SAVEPOINT s1;")
    raise e

# Comprobar que hay suficiente saldo
try:
    cur.execute(f"SELECT saldo FROM cuenta WHERE idcuenta = {id_origen} FOR UPDATE;")
    saldo = cur.fetchone()[0]
    if saldo < cantidad:
        raise Exception("No hay suficiente saldo")
except Exception as e:
    cur.execute("ROLLBACK TO SAVEPOINT s1;")
    cur.execute("RELEASE SAVEPOINT s1;")
    raise e

# Obtener el identificador de la nueva transacción
cur.execute(f"SELECT MAX(idmov) FROM movimiento;")
last_idmove = cur.fetchone()[0]
if last_idmove is None:
    last_idmove = 0
else:
    last_idmove = int(last_idmove)
new_idmov = last_idmove + 1

# Comenzar la transferencia

# Primer paso: retirar el dinero de la cuenta origen
try:
    cur.execute(f"UPDATE cuenta SET saldo = saldo - {cantidad} WHERE idcuenta = {id_origen};")
except Exception as e:
    cur.execute("ROLLBACK TO SAVEPOINT s1;")
    cur.execute("RELEASE SAVEPOINT s1;")
    raise e

# Segundo paso: ingresar el dinero en la cuenta destino
# Preguntar al usuario si quiere continuar
print("Dinero retirado de la cuenta origen")
resp = input(f"¿Seguro que quiere ingresar el dinero en la cuenta {id_destino}? (s/n): ")
if resp != 's':
    # Si el usuario no quiere continuar, deshacer los cambios
    cur.execute("ROLLBACK TO SAVEPOINT s1;")
    cur.execute("RELEASE SAVEPOINT s1;")
    raise Exception("Operación cancelada por el usuario")
else:
    # Si el usuario quiere continuar, hacer los cambios
    try:
        cur.execute(f"UPDATE cuenta SET saldo = saldo + {cantidad} WHERE idcuenta = {id_destino};")
        cur.execute(f"INSERT INTO movimiento (idmov, idcuenta, cantidad) VALUES ({new_idmov}, {id_origen}, {-cantidad});")
        cur.execute(f"INSERT INTO movimiento (idmov, idcuenta, cantidad) VALUES ({new_idmov+1}, {id_destino}, {cantidad});")
        conn.commit()
    except Exception as e:
        cur.execute("ROLLBACK TO SAVEPOINT s1;")
        cur.execute("RELEASE SAVEPOINT s1;")
        raise e
    print("Dinero ingresado en la cuenta destino")
    cur.close()
