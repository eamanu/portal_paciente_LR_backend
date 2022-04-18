from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config.database import SessionLocal
from app.gear.local.local_impl import LocalImpl
from app.gear.log.main_logger import MainLogger, logging
from sqlalchemy.orm import Session

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

app = FastAPI(title="Portal del paciente",
              description="Interfaz de programación para exponer información relativa al paciente.",
              version="0.0.1")

log = MainLogger()
module = logging.getLogger(__name__)
db: Session = SessionLocal()

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


@app.middleware("http")
async def filter_request_for_authorization(request: Request, call_next):
    return await LocalImpl().filter_request_for_authorization(request, call_next)


"""
from fastapi import File, UploadFile
from app.config.config import LOCAL_FILE_UPLOAD_DIRECTORY
import aiofiles
import base64
from app.models.person import Person as model_person


@app.post("/portalpaciente/api/v1/uploadidentificationimages")
async def upload_identification_images(person_id: str, file: UploadFile = File(...),
                                       file2: UploadFile = File(...)):
    b64_string_file1 = ""
    b64_string_file2 = ""

    try:

        # File 1 ------------------------------------------------------------------------------------
        destination_file_path = LOCAL_FILE_UPLOAD_DIRECTORY + file.filename  # location to store file

        file_a = open(destination_file_path, "wb+")

        file_a.write(await file.read())

        file_a.close()

        with open(destination_file_path, "rb") as bin_file:
            b64_string_file1 = base64.b64encode(bin_file.read())

        # File 2 ------------------------------------------------------------------------------------
        destination_file_path = LOCAL_FILE_UPLOAD_DIRECTORY + file2.filename  # location to store file

        file_b = open(destination_file_path, "wb+")

        file_b.write(await file2.read())

        file_b.close()

        with open(destination_file_path, "rb") as bin_file:
            b64_string_file2 = base64.b64encode(bin_file.read())

        # Saving process -----------------------------------------------------------------------------
        existing_person = (db.query(model_person).where(model_person.id == person_id).first())

        existing_person.identification_front_image = b64_string_file1
        existing_person.identification_back_image = b64_string_file2

        db.commit()

    except Exception as e:
        log.log_error_message(e, module)
        print(e)

    print("ESTOY ACÁ FINALIZANDO...")
    return {"Result": "OK"}
"""
