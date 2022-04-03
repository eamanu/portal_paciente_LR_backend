from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import SessionLocal
from app.gear.local.local_impl import LocalImpl

# region Dependency

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# endregion


from app.routes.hsi import hsi
from app.routes.local import local
from app.routes.local import admin

app = FastAPI(title="Portal del paciente",
              description="Interfaz de programación para exponer información relativa al paciente.",
              version="0.0.1")

# region CORS

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# endregion

app.include_router(hsi.router_hsi)
app.include_router(local.router_local)
app.include_router(admin.router_admin)



@app.middleware("http")
async def filter_request_for_authorization(request: Request, call_next):
    return await LocalImpl().filter_request_for_authorization(request, call_next)
