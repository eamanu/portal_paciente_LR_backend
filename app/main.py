from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import SessionLocal
from app.gear.local.local_impl import LocalImpl
from app.gear.log.main_logger import MainLogger, logging


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
from app.routes.sumar import sumar
from app.config.config import LR_BASE_API

app = FastAPI(
    title="Portal del paciente",
    description="Interfaz de programación para exponer información relativa al paciente.",
    version="0.0.1",
)

log = MainLogger()
module = logging.getLogger(__name__)

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
app.include_router(sumar.router_sumar)

from fastapi.staticfiles import StaticFiles
from app.config.config import LOCAL_FILE_DOWNLOAD_DIRECTORY


@app.middleware("http")
async def filter_request_for_authorization(request: Request, call_next):
    db = next(get_db())
    return await LocalImpl(db).filter_request_for_authorization(request, call_next)


app.mount(
    LR_BASE_API + "/static",
    StaticFiles(directory=LOCAL_FILE_DOWNLOAD_DIRECTORY, html=True),
    name="static",
)
