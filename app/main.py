from fastapi import FastAPI

from app.routes import institutions
from app.routes import persons

app = FastAPI()


app.include_router(institutions.router)
app.include_router(persons.router)


@app.get("/")
async def root():
    return {"message": "Bienvenido al Portal de Pacientes de La Rioja"}
