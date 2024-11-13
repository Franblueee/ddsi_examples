# import sqlite3

import psycopg2 as pg
import psycopg2.extras as extras


from flask import Blueprint
import click
from flask import current_app
from flask import g

from flask import url_for, redirect

bp = Blueprint("db", __name__, url_prefix="/db")

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        # g.db = sqlite3.connect(
        #     current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.row_factory = sqlite3.Row

        g.db = pg.connect(
            database='banco',
            user='fran',
            password='fran',
            host='localhost',
        )
        g.db.autocommit = False

    return g.db

def get_db_cursor():
    db = get_db()
    return db.cursor(cursor_factory=extras.RealDictCursor)


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    cur = get_db_cursor()
    with current_app.open_resource("schema.sql") as f:
        # db.executescript(f.read().decode("utf8"))
        cur.execute(f.read().decode("utf8"))
        cur.execute("COMMIT;")


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

@bp.route("/init_db_from_app", methods=("GET", "POST"))
def init_db_from_app():
    init_db()
    return redirect(url_for("movimientos.index"))


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
