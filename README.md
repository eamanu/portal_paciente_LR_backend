# Portal Pacientes La Rioja - Backend

TODO

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
