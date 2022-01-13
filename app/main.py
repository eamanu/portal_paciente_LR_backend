from fastapi import FastAPI
from app.database import SessionLocal


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


from app.routes.hsi import hsi
from app.routes import auth


app = FastAPI(title="Portal del paciente",
              description="Interfaz de programación para exponer información relativa al paciente.",
              version="0.0.1")


app.include_router(hsi.router_hsi)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Bienvenido al Portal de Pacientes de La Rioja"}
