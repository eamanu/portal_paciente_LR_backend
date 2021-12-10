from fastapi import FastAPI
from app.routes import institutions


app = FastAPI()


app.include_router(institutions.router)


@app.get("/")
async def root():
    return {"message": "Bienvenido al Portal de Pacientes de La Rioja"}
