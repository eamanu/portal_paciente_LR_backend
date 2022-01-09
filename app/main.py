from fastapi import FastAPI

from app.routes.hsi import hsi

app = FastAPI(title="Portal del paciente",
              description="Interfaz de programación para exponer información relativa al paciente.",
              version="0.0.1")

app.include_router(hsi.router_hsi)


@app.get("/")
async def root():
    return {"message": "Bienvenido al Portal de Pacientes de La Rioja"}
