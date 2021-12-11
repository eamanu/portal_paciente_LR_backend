from typing import Dict

from fastapi import APIRouter

from app.hsi.persons import HSIPersons

router = APIRouter(
    prefix="/hsi/api/v1/patient",
    tags=["patient"],
    responses={404: {"description": "Not Found"}}
)


@router.get("/completedata")
async def complete_data(gender_id: int, id_number: int,
                        id_type: int) -> Dict:
    patient = HSIPersons()
    id_patient = patient.minimal_search(gender_id, id_number, id_type)[0]

    return patient.get_patient_complete_data(id_patient)
