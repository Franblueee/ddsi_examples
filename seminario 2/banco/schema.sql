-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS cuenta CASCADE;
DROP TABLE IF EXISTS movimiento CASCADE;

CREATE TABLE IF NOT EXISTS cuenta(
    idcuenta SERIAL PRIMARY KEY,
    saldo FLOAT
);

CREATE TABLE IF NOT EXISTS movimiento(
    idmov SERIAL PRIMARY KEY,
    idcuenta INTEGER,
    cantidad FLOAT,
    FOREIGN KEY(idcuenta) REFERENCES cuenta(idcuenta)
);

INSERT INTO cuenta VALUES (1, 1000);
INSERT INTO cuenta VALUES (2, 2000);
INSERT INTO cuenta VALUES (3, 3000);
INSERT INTO cuenta VALUES (4, 4000);
