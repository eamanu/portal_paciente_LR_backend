from fastapi import FastAPI, Request
from app.config.database import SessionLocal
from app.gear.local.local_impl import LocalImpl

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


from app.routes.hsi import hsi
from app.routes.local import local


app = FastAPI(title="Portal del paciente",
              description="Interfaz de programación para exponer información relativa al paciente.",
              version="0.0.1")

app.include_router(hsi.router_hsi)
app.include_router(local.router_local)


@app.middleware("http")
async def filter_request_for_authorization(request: Request, call_next):
    return await LocalImpl().filter_request_for_authorization(request, call_next)


@app.get("/")
async def root():
    return {"message": "Bienvenido al Portal de Pacientes de La Rioja"}
