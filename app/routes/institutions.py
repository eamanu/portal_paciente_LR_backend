from fastapi import APIRouter
from app.hsi.institutions import HSIInstitutions
from typing import Dict

router = APIRouter(
    prefix="/hsi/api/v1/institution",
    tags=["institutions"],
    responses={404: {"description": "Not Found"}}
)


@router.get("/all")
async def all_institutions() -> Dict:
    hsi_institutions = HSIInstitutions()
    return hsi_institutions.get_all_institutions()
