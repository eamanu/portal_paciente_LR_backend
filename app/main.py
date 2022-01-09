from fastapi import FastAPI
from app.database import SessionLocal


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


from app.routes import (
    hce_general,
    institutions,
    persons,
    auth,
)

app = FastAPI()

app.include_router(institutions.router)
app.include_router(persons.router)
app.include_router(hce_general.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Bienvenido al Portal de Pacientes de La Rioja"}
