from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from .db import get_db_cursor

bp = Blueprint("movimientos", __name__)


@bp.route("/")
def index():
    """
    Muestra todos los movimientos
    """
    cur = get_db_cursor()
    cur.execute(
        "SELECT * FROM cuenta ORDER BY idcuenta"
    )
    cuentas = cur.fetchall()
    cur.execute(
        "SELECT * FROM movimiento"
    )
    movimientos = cur.fetchall()
    return render_template("movimientos/index.html", movimientos=movimientos, cuentas=cuentas)


@bp.route("/create", methods=("GET", "POST"))
def create():
    """
    Crea un nuevo movimiento.
    """
    if request.method == "POST":
        cuenta_origen = request.form.get("cuenta_origen", default=-1, type=int)
        cuenta_destino = request.form.get("cuenta_destino", default=-1, type=int)
        cantidad = request.form.get("cantidad", default=0.0, type=float)
        
        error = None

        if not cuenta_destino:
            error = "Falta la cuenta de destino."
        
        if not cuenta_origen or cuenta_origen < 0:
            error = "Falta la cuenta de origen."

        if not cantidad:
            error = "Falta la cantidad."

        if error is not None:
            flash(error)
            return render_template("movimientos/create.html")

        error = None
        # Comprobar que las cuentas existen
        cur = get_db_cursor()
        cur.execute(f"SELECT idcuenta FROM cuenta WHERE idcuenta = {cuenta_origen}")
        data = cur.fetchall()
        if len(data) == 0:
            error = "La cuenta de origen no existe"
            flash(error)
            return render_template("movimientos/create.html")

        cur.execute(f"SELECT idcuenta FROM cuenta WHERE idcuenta = {cuenta_destino}")
        data = cur.fetchall()
        if len(data) == 0:
            error = "La cuenta de destino no existe"
            flash(error)
            return render_template("movimientos/create.html")

        # Comprobar que hay suficiente saldo
        cur.execute(f"SELECT saldo FROM cuenta WHERE idcuenta = {cuenta_origen}")
        saldo = cur.fetchone()['saldo']
        if saldo < cantidad:
            error = "No hay suficiente saldo en la cuenta de origen"
            flash(error)
            return render_template("movimientos/create.html")
        
        # Retirar el dinero de la cuenta origen
        cur.execute(
            f"INSERT INTO movimiento (idcuenta, cantidad) VALUES ({cuenta_origen}, {-cantidad})"
        )

        # Ingresar el dinero en la cuenta destino
        cur.execute(
            f"INSERT INTO movimiento (idcuenta, cantidad) VALUES ({cuenta_destino}, {cantidad})"
        )

        # Actualizar los saldos
        cur.execute(
            f"UPDATE cuenta SET saldo = saldo - {cantidad} WHERE idcuenta = {cuenta_origen}"
        )

        # Actualizar los saldos
        cur.execute(
            f"UPDATE cuenta SET saldo = saldo + {cantidad} WHERE idcuenta = {cuenta_destino}"
        )

        cur.execute("COMMIT;")
        return redirect(url_for("movimientos.index"))

    return render_template("movimientos/create.html")

