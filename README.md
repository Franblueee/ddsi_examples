# DDSI

[English] This repository contains the support material developed for the subject Design and Development of Information Systems (DDSI) at the University of Granada (UGR). This material was developed during the time I taught this subject. It is addressed to the students of this subject, so it is completely in Spanish. 

[Español] En este repositorio se recoge el material de apoyo desarrollado para la asignatura de Diseño y Desarrollo de Sistemas de Información (DDSI) de la Universidad de Granada (UGR). Este material fue desarrollado durante el tiempo que impartí las prácticas de esta asignatura. 

## Instalación de PostgreSQL en Anaconda

**Paso 1.** Creación de un entorno virtual de Anaconda. Instalamos Anaconda desde [aquí](https://www.anaconda.com/products/individual). Una vez instalado, abrimos un terminal y ejecutamos los siguientes comandos:
```bash
conda create -n DDSI python=3.9 # Crear entorno virtual
conda activate DDSI # Activar entorno virtual
conda install -c anaconda postgresql # Instalar PostgreSQL
conda install -c anaconda psycopg2 # Instalar driver de Python para PostgreSQL
pip install Flask # Instalar Flask (seminario 2)
```

**Paso 2.** Inicialización de PostgreSQL y creación de una base de datos. Para ello, abrimos un terminal y ejecutamos los siguientes comandos:
```bash
conda activate DDSI # Activar entorno virtual
initdb ./pgdata # Crear database cluster directory
pg_ctl -D ./pgdata -l logfile start # Iniciar PostgreSQL
```

El comando `pg_ctl` crea un directorio llamado `pgdata` en el directorio actual. Este directorio contiene los archivos de configuración de PostgreSQL. Se puede sustituir `./pgdata` por cualquier otro directorio. El comando `pg_ctl` también inicia el servidor de PostgreSQL. Para detener el servidor, ejecutamos el siguiente comando:
```bash
pg_ctl -D ./pgdata stop # Detener PostgreSQL
```

En este punto, ya podemos iniciar sesión en PostgreSQL conectándonos a una base de datos:
```bash
psql -l # Listar bases de datos
psql -d postgres # Conectarse a la base de datos postgres
```

Una vez dentro de PostgreSQL, debemos crear un nuevo usuario y darle permisos de SUPERUSUARIO:
```bash
CREATE USER usuario WITH PASSWORD 'password'; # Crear usuario
ALTER USER usuario WITH SUPERUSER; # Dar permisos de superusuario al usuario
\q # Salir de PostgreSQL
```

También podemos crear una base de datos y una tabla:
```bash
\c postgres # Conectarse a la base de datos postgres
CREATE DATABASE test; # Crear base de datos test
\c test # Conectarse a la base de datos test
\i create_table.sql # Ejecutar script de SQL para crear tabla
\l # Listar bases de datos
\dt # Listar tablas
\q # Salir de PostgreSQL
```

## Seminario 1

Para poder ejecutar el ejemplo correspondiente al Seminario 1 tendremos que crear la base de datos "banco". Después, tenemos que inicializar el estado de la base de datos mediante el script crear_banco.sql, que se encuentra en la carpeta `seminario1`. 
```bash
\c postgres # Conectarse a la base de datos postgres
CREATE DATABASE banco; # Crear base de datos test
\c banco # Conectarse a la base de datos test
\i crear_banco.sql # Ejecutar script de SQL para crear tabla
```
No te olvides de modificar el fichero `ejemplo.py` con los datos de tu usuario y contraseña de PostgreSQL.

## Seminario 2

Para poder ejecutar el ejemplo correspondiente al Seminario 2 tendremos que crear la base de datos "banco" (si no la hemos creado ya) e instalar `Flask` en el entorno de Anaconda (si no lo hemos instalado ya). Después, podremos ejecutar las dos aplicaciones web que se encuentran en la carpeta `seminario2`. 

"flaskr" se ha creado siguiendo el tutorial de Flask que se encuentra en la [documentación oficial](https://flask.palletsprojects.com/en/stable/tutorial/). Para ejecutar la aplicación web, abrimos un terminal y ejecutamos los siguientes comandos:
```bash
flask --app flaskr init-db # Inicializar base de datos
flask --app flaskr run # Ejecutar aplicación web
```

"banco" se ha creado a partir de "flaskr" y otorga una interfaz web a las funcionalidades del script del seminario 1. Para ejecutar la aplicación web, abrimos un terminal y ejecutamos los siguientes comandos:
```bash
flask --app banco init-db # Inicializar base de datos
flask --app banco run # Ejecutar aplicación web
```
