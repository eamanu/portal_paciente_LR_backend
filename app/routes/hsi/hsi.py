from app.gear.hsi.hsi_impl import HSI_Impl
from typing import Dict
from app.routes.common import router_hsi

###############################################################################
## Parametric data ############################################################
###############################################################################

@router_hsi.get("/parametric/identificationtypes", tags=['Parametric'])
async def get_identification_types() -> Dict:
    hsi_impl = HSI_Impl()
    return hsi_impl.get_identification_types()


@router_hsi.get("/parametric/provinces", tags=['Parametric'])
async def get_provinces() -> Dict:
    hsi_impl = HSI_Impl()
    return hsi_impl.get_provinces()

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

@router_hsi.get("/patient/basicdata", tags=['Patient'])
async def basic_data(gender_id: int, identification_number: int, type_id: int) -> Dict:
    hsi_impl = HSI_Impl()
    arr = hsi_impl.minimal_search(gender_id, identification_number, type_id)

    if arr != []:
        id_patient = arr[0]
        return hsi_impl.get_patient_basic_data(id_patient)
    else:
        return ""

@router_hsi.get("/patient/completedata", tags=['Patient'])
async def complete_data(gender_id: int, identification_number: int,
                        type_id: int) -> Dict:
    hsi_impl = HSI_Impl()
    ids_patient = hsi_impl.minimal_search(gender_id, identification_number, type_id)

    if ids_patient != []:
        id_patient = ids_patient[0]
        return hsi_impl.get_patient_complete_data(id_patient)
    else:
        return ""

