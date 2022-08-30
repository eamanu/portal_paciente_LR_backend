# Portal Pacientes La Rioja - Backend

## Requerimientos

Python 3.9+

## Levantar la app para desarrollo

Para levantar la aplicación para desarrollo, se debe seguir los siguientes pasos
en la línea de comandos:

```python
python3 -m venv venv  # crear un entorno virtual
source venv/bin/activate  # ingresar al entorno virtual
python install -r requirements.txt # instalar los requerimientos

uvicorn app.main:app --reload
```

Esto se encuentra detallado en (FastAPI documentation)[https://fastapi.tiangolo.com/tutorial/first-steps/]

## Swagger
Se puede encontrar documentación de esta API en ``localhost:8000/docs`` (previamente debe estar levantada
la aplicación).

# HSI
Para ejecutar las api de HSI se deben setear las siguientes variables de entorno:

  * HSI_USERNAME
  * HSI_PASSWORD

# Uso de docker-compose
Para levantar la aplicación haciendo uso de Docker Compose es necesario
tener instalado Docker y Docker Compose.

Primero se debe crear los archivos que contienen las variables de 
entorno, uno para backend (`.env_backend`) y otro para la base de datos
(`.env_database`) con la siguiente información:

#### .env_backend
HSI_USERNAME=<hsi_user>
HSI_PASSWORD=<hsi_password>
DATABASE_URL=mysql+pymysql://<user>:<password>@portal_pacientes_db:3306/portal_paciente_LR

#### .env_database
MYSQL_ROOT_PASSWORD=<pass>
MYSQL_DATABASE=portal_paciente_LR
MYSQL_USER=<user>
MYSQL_PASSWORD=<user>

Luego se debe levantar utilizando el siguiente [docker-compose](https://github.com/eamanu/portal_pacientes_docker-compose/blob/main/docker-compose.yml). Se recomienda buildear las imagenes localmente.

```bash
$ docker-compose up -d
```

Este docker-compose levanta un MariaDB y el Backend, además de Adminer para
la gestión de la base de datos. Si no se quiere instalar Adminer eliminar el 
servicio del docker-compose.

Luego debemos rellenar la base de datos ejecutando el siguiente commando:

```bash
$ cat database/initfile.sql | docker exec -i portal_pacientes_db /usr/bin/mysql -u root  --password=root portal_paciente_LR
```
