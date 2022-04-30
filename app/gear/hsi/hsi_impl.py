import json
from typing import Dict, List

import requests

from app.gear import config
from app.gear.hsi.hsi_token import HSIToken


class HSI_Impl:
    def __init__(self):
        self.token = HSIToken().connect().token

    # region General

    @property
    def headers(self):
        return {"accept": "*/*",
                "Accept-Encoding": "deflate",
                "Authorization": self.token}

    def get_generic(self, endpoint, payload=None) -> Dict:
        if payload is None:
            req = requests.get(endpoint, headers=self.headers)
        else:
            req = requests.get(endpoint, headers=self.headers, params=payload)
        return json.loads(req.text)

    # endregion

    # region Parametric data

    def get_identification_types(self) -> Dict:
        return self.get_generic(config.ALL_IDENTIFICATION_TYPES)

    def get_provinces(self) -> Dict:
        return self.get_generic(config.ALL_PROVINCES)

    # endregion

    # region HCEGeneral

    def get_allergies(self, institution_id, patient_id) -> Dict:
        return self.get_generic(config.HCE_ALLERGIES.format(institutionId=institution_id, patientId=patient_id))

    def get_anthropometric_data(self, institution_id, patient_id) -> Dict:
        return self.get_generic(config.HCE_ANTHROPOMETRIC_DATA.format(institutionId=institution_id, patientId=patient_id))

    def get_chronic(self, institution_id, patient_id) -> Dict:
        return self.get_generic(config.HCE_CHRONIC_DATA.format(institutionId=institution_id, patientId=patient_id))

    def get_family_histories(self, institution_id, patient_id) -> Dict:
        return self.get_generic(config.HCE_FAMILY_HISTORIES.format(institutionId=institution_id, patientId=patient_id))

    def get_hospitalization(self, institution_id, patient_id) -> Dict:
        return self.get_generic(config.HCE_HOSPITALIZATION.format(institutionId=institution_id, patientId=patient_id))

    def get_immunizations(self, institution_id, patient_id) -> Dict:
        return self.get_generic(config.HCE_IMMUNIZATIONS.format(institutionId=institution_id, patientId=patient_id))

    def get_medications(self, institution_id, patient_id) -> Dict:
        return self.get_generic(config.HCE_MEDICATIONS.format(institutionId=institution_id, patientId=patient_id))

    def get_personal_histories(self, institution_id, patient_id) -> Dict:
        return self.get_generic(config.HCE_PERSONAL_HISTORIES.format(institutionId=institution_id, patientId=patient_id))

    def get_tooth_records(self, institution_id, patient_id, tooth_sct_id) -> Dict:
        return self.get_generic(config.HCE_TOOTH_RECORDS.format(institutionId=institution_id, patientId=patient_id, toothSctid=tooth_sct_id))

    def get_active_problems(self, institution_id, patient_id) -> Dict:
        return self.get_generic(config.HCE_ACTIVE_PROBLEMS.format(institutionId=institution_id, patientId=patient_id))

    def get_solved_problems(self, institution_id, patient_id) -> Dict:
        return self.get_generic(config.HCE_SOLVED_PROBLEMS.format(institutionId=institution_id, patientId=patient_id))

    def get_vital_signs(self, institution_id, patient_id) -> Dict:
        return self.get_generic(config.HCE_VITAL_SIGNS.format(institutionId=institution_id, patientId=patient_id))

    # endregion

    # region Institutions

    def get_all_institutions(self):
        return self.get_generic(config.ALL_INSTITUTIONS)

    # endregion

    # region Patient

    def minimal_search(self, gender_id: int, identification_number: int, type_id: int) -> List:
        return self.get_generic(config.MINIMAL_SEARCH, {"genderId": gender_id, "identificationTypeId": type_id, "identificationNumber": identification_number})

    def get_patient_basic_data(self, patient_id: int) -> Dict:
        return self.get_generic(config.PATIENT_BASIC_DATA % patient_id)

    def get_patient_complete_data(self, patient_id: int) -> Dict:
        return self.get_generic(config.PATIENT_COMPLETE_DATA % patient_id)

    # endregion
