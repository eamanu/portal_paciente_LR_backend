from app.gear.hsi.hsi_impl import HSI_Impl
from typing import Dict
from app.routes.common import router_hsi

###############################################################################
## HCEGeneral #################################################################
###############################################################################

@router_hsi.get("/hcegeneral/{institution_id}/vitalsigns/{patient_id}", tags=['HCEGeneral'])
async def get_vital_signs(institution_id: int, patient_id: int) -> Dict:
    hsi_impl = HSI_Impl()
    return hsi_impl.get_vital_signs(institution_id, patient_id)


@router_hsi.get("/hcegeneral/{institution_id}/solvedproblems/{patient_id}", tags=['HCEGeneral'])
async def get_solved_problems(institution_id: int, patient_id: int) -> Dict:
    hsi_impl = HSI_Impl()
    return hsi_impl.get_solved_problems(institution_id, patient_id)


###############################################################################
## Institutions ###############################################################
###############################################################################

@router_hsi.get("/institutions/all", tags=['Institutions'])
async def all_institutions() -> Dict:
    hsi_impl = HSI_Impl()
    return hsi_impl.get_all_institutions()



###############################################################################
## Patient ####################################################################
###############################################################################

@router_hsi.get("/patient/completedata", tags=['Patient'])
async def complete_data(gender_id: int, id_number: int,
                        id_type: int) -> Dict:
    hsi_impl = HSI_Impl()
    id_patient = hsi_impl.minimal_search(gender_id, id_number, id_type)[0]

    return hsi_impl.get_patient_complete_data(id_patient)

