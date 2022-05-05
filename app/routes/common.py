from fastapi import APIRouter
from app.config.config import LR_BASE_API


router_hsi = APIRouter(
    prefix=LR_BASE_API,
    responses={404: {"description": "Not Found"}}
)


router_local = APIRouter(
    prefix=LR_BASE_API,
    responses={404: {"description": "Not Found"}}
)

router_admin = APIRouter(
    tags=["Admin"],
    prefix=LR_BASE_API,
    responses={404: {"description": "Not Found"}}
)

router_sumar = APIRouter(
    tags=["SUMAR"],
    prefix=LR_BASE_API,
    responses={404: {"description": "Not Found"}}
)
