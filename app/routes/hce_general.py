from fastapi import APIRouter
from app.hsi.hce_general_state import HCEGeneralState
from typing import Dict

router = APIRouter(
    prefix="/hsi/api/v1/hcegeneral",
    tags=["HCEGeneral"],
    responses={404: {"description": "Not Found"}}
)


@router.get("/{institution_id}/vitalsigns/{patient_id}")
async def get_vital_signs(institution_id: int, patient_id: int) -> Dict:
    hce_general_signs = HCEGeneralState()
    return hce_general_signs.get_vital_signs(institution_id, patient_id)
