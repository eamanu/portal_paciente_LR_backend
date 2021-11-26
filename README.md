# Portal Pacientes La Rioja - Backend

TODO

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

