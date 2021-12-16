from fastapi import FastAPI

from app.routes import (
    hce_general,
    institutions,
    persons
)

app = FastAPI()

app.include_router(institutions.router)
app.include_router(persons.router)
app.include_router(hce_general.router)


@app.get("/")
async def root():
    return {"message": "Bienvenido al Portal de Pacientes de La Rioja"}
