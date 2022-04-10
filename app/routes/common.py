from fastapi import APIRouter


router_hsi = APIRouter(
    prefix="/portalpaciente/api/v1",
    responses={404: {"description": "Not Found"}}
)


router_local = APIRouter(
    prefix="/portalpaciente/api/v1",
    responses={404: {"description": "Not Found"}}
)

router_admin = APIRouter(
    tags=["Admin"],
    prefix="/portalpaciente/api/v1/admin",
    responses={404: {"description": "Not Found"}}
)

router_sumar = APIRouter(
    tags=["SUMAR"],
    prefix="/portalpaciente/api/v1/sumar",
    responses={404: {"description": "Not Found"}}
)
