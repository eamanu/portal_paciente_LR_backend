from typing import Dict

from fastapi.encoders import jsonable_encoder

from app.gear.hsi.hsi_impl import HSI_Impl
from app.gear.hsi.hsi_impl_2 import HSIImpl2
from app.routes.common import router_hsi


# region Parametric data


@router_hsi.get("/parametric/identificationtypes", tags=["Parametric"])
async def get_identification_types() -> Dict:
    hsi_impl = HSI_Impl()
    return hsi_impl.get_identification_types()


@router_hsi.get("/parametric/provinces", tags=["Parametric"])
async def get_provinces() -> Dict:
    hsi_impl = HSI_Impl()
    return hsi_impl.get_provinces()


# endregion

# region HCEGeneral


#@router_hsi.get(
#    "/hcegeneral/{institution_id}/allergies/{patient_id}", tags=["HCEGeneral"]
#)
#async def get_allergies_old(institution_id: int, patient_id: int) -> Dict:
#    hsi_impl = HSI_Impl()
#    return hsi_impl.get_allergies(institution_id, patient_id)


#@router_hsi.get(
#    "/hcegeneral/{institution_id}/anthropometricData/{patient_id}", tags=["HCEGeneral"]
#)
#async def get_anthropometric_data(institution_id: int, patient_id: int) -> Dict:
#    hsi_impl = HSI_Impl()
#    return hsi_impl.get_anthropometric_data(institution_id, patient_id)


#@router_hsi.get(
#    "/hcegeneral/{institution_id}/chronic/{patient_id}", tags=["HCEGeneral"]
#)
#async def get_chronic(institution_id: int, patient_id: int) -> Dict:
#    hsi_impl = HSI_Impl()
#    return hsi_impl.get_chronic(institution_id, patient_id)


@router_hsi.get(
    "/hcegeneral/{institution_id}/familyHistories/{patient_id}", tags=["HCEGeneral"]
)
async def get_family_histories(institution_id: int, patient_id: int) -> Dict:
    hsi_impl = HSI_Impl()
    return hsi_impl.get_family_histories(institution_id, patient_id)


@router_hsi.get(
    "/hcegeneral/{institution_id}/hospitalization/{patient_id}", tags=["HCEGeneral"]
)
async def get_hospitalization(institution_id: int, patient_id: int) -> Dict:
    hsi_impl = HSI_Impl()
    return hsi_impl.get_hospitalization(institution_id, patient_id)


#@router_hsi.get(
#    "/hcegeneral/{institution_id}/immunizations/{patient_id}", tags=["HCEGeneral"]
#)
#async def get_immunizations(institution_id: int, patient_id: int) -> Dict:
#    hsi_impl = HSI_Impl()
#    return hsi_impl.get_immunizations(institution_id, patient_id)


#@router_hsi.get(
#    "/hcegeneral/{institution_id}/medications/{patient_id}", tags=["HCEGeneral"]
#)
#async def get_medications(institution_id: int, patient_id: int) -> Dict:
#    hsi_impl = HSI_Impl()
#    return hsi_impl.get_medications(institution_id, patient_id)


@router_hsi.get(
    "/hcegeneral/{institution_id}/personalHistories/{patient_id}", tags=["HCEGeneral"]
)
async def get_personal_histories(institution_id: int, patient_id: int) -> Dict:
    hsi_impl = HSI_Impl()
    return hsi_impl.get_personal_histories(institution_id, patient_id)


#@router_hsi.get(
#    "/hcegeneral/{institution_id}/toothRecords/{patient_id}/tooth/{tooth_sct_id}",
#    tags=["HCEGeneral"],
#)
#async def get_tooth_records(
#    institution_id: int, patient_id: int, tooth_sct_id: str
#) -> Dict:
#    hsi_impl = HSI_Impl()
#    return hsi_impl.get_tooth_records(institution_id, patient_id, tooth_sct_id)


#@router_hsi.get(
#    "/hcegeneral/{institution_id}/activeProblems/{patient_id}", tags=["HCEGeneral"]
#)
#async def get_active_problems(institution_id: int, patient_id: int) -> Dict:
#    hsi_impl = HSI_Impl()
#    return hsi_impl.get_active_problems(institution_id, patient_id)


#@router_hsi.get(
#    "/hcegeneral/{institution_id}/solvedProblems/{patient_id}", tags=["HCEGeneral"]
#)
#async def get_solved_problems(institution_id: int, patient_id: int) -> Dict:
#    hsi_impl = HSI_Impl()
#    return hsi_impl.get_solved_problems(institution_id, patient_id)


#@router_hsi.get(
#    "/hcegeneral/{institution_id}/vitalSigns/{patient_id}", tags=["HCEGeneral"]
#)
#async def get_vital_signs(institution_id: int, patient_id: int) -> Dict:
#    hsi_impl = HSI_Impl()
#    return hsi_impl.get_vital_signs(institution_id, patient_id)


# endregion

# region Institutions


@router_hsi.get("/institutions/all", tags=["Institutions"])
async def all_institutions() -> Dict:
    hsi_impl = HSI_Impl()
    return hsi_impl.get_all_institutions()


# endregion

# region Patient


@router_hsi.get("/patient/basicData", tags=["Patient"])
async def basic_data(gender_id: int, identification_number: int, type_id: int) -> Dict:
    hsi_impl = HSI_Impl()
    arr = hsi_impl.minimal_search(gender_id, identification_number, type_id)

    if arr:
        id_patient = arr[0]
        return hsi_impl.get_patient_basic_data(id_patient)
    else:
        return {}


@router_hsi.get("/patient/completeData", tags=["Patient"])
async def complete_data(
    gender_id: int, identification_number: int, type_id: int
) -> Dict:
    hsi_impl = HSI_Impl()
    ids_patient = hsi_impl.minimal_search(gender_id, identification_number, type_id)

    if ids_patient:
        id_patient = ids_patient[0]
        return hsi_impl.get_patient_complete_data(id_patient)
    else:
        return {}


# endregion


# TODO: REMOVE THIS TEST
# region test

@router_hsi.get("/tests/bed", tags=["TESTS"])
def complete_data():
    hsi_impl = HSIImpl2()
    return hsi_impl.execute("SELECT * FROM bed")

# endregion

@router_hsi.get(
    "/hcegeneral/{institution_id}/allergies/{patient_id}", tags=["HCEGeneral"]
)
def get_allergies(institution_id: int, patient_id: int):
    hsi_impl = HSIImpl2()
    return hsi_impl.get_allergies(institution_id, patient_id)

@router_hsi.get(
    "/hcegeneral/{institution_id}/anthropometricData/{patient_id}", tags=["HCEGeneral"]
)
async def get_anthropometric_data(institution_id: int, patient_id: int) -> Dict:
    hsi_impl = HSIImpl2()
    return hsi_impl.get_anthropometric_data(institution_id, patient_id)

@router_hsi.get(
    "/hcegeneral/{institution_id}/chronic/{patient_id}", tags=["HCEGeneral"]
)
async def get_chronic(institution_id: int, patient_id: int) -> Dict:
    hsi_impl = HSIImpl2()
    return hsi_impl.get_chronic(institution_id, patient_id)

@router_hsi.get(
    "/hcegeneral/{institution_id}/immunizations/{patient_id}", tags=["HCEGeneral"]
)
async def get_immunizations(institution_id: int, patient_id: int) -> Dict:
    hsi_impl = HSIImpl2()
    return hsi_impl.get_immunizations(institution_id, patient_id)


@router_hsi.get(
    "/hcegeneral/{institution_id}/medications/{patient_id}", tags=["HCEGeneral"]
)
async def get_medications(institution_id: int, patient_id: int) -> Dict:
    hsi_impl = HSIImpl2()
    return hsi_impl.get_medications(institution_id, patient_id)

@router_hsi.get(
    "/hcegeneral/{institution_id}/toothRecords/{patient_id}/tooth/{tooth_sct_id}",
    tags=["HCEGeneral"],
)
async def get_tooth_records(
    institution_id: int, patient_id: int, tooth_sct_id: str
) -> Dict:
    hsi_impl = HSIImpl2()
    return hsi_impl.get_tooth_records(institution_id, patient_id, tooth_sct_id)


@router_hsi.get(
    "/hcegeneral/{institution_id}/activeProblems/{patient_id}", tags=["HCEGeneral"]
)
async def get_active_problems(institution_id: int, patient_id: int) -> Dict:
    hsi_impl = HSIImpl2()
    return hsi_impl.get_active_problems(institution_id, patient_id)


@router_hsi.get(
    "/hcegeneral/{institution_id}/solvedProblems/{patient_id}", tags=["HCEGeneral"]
)
async def get_solved_problems(institution_id: int, patient_id: int) -> Dict:
    hsi_impl = HSIImpl2()
    return hsi_impl.get_solved_problems(institution_id, patient_id)


@router_hsi.get(
    "/hcegeneral/{institution_id}/vitalSigns/{patient_id}", tags=["HCEGeneral"]
)
async def get_vital_signs(institution_id: int, patient_id: int) -> Dict:
    hsi_impl = HSIImpl2()
    return hsi_impl.get_vital_signs(institution_id, patient_id)

