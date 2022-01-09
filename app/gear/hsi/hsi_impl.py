import json
from typing import Dict, List

import requests

from app.gear import config
from app.gear.hsi.hsi_token import HSIToken


class HSI_Impl:
    def __init__(self):

        self.token = HSIToken().connect().token



    @property
    def headers(self):
        return {"accept": "*/*", "Authorization": self.token}


    ###############################################################################
    ## HCEGeneral #################################################################
    ###############################################################################

    def get_vital_signs(self, institution_id, patient_id) -> Dict:
        endpoint = config.HCE_VITAL_SIGNS.format(institutionId=institution_id, patientId=patient_id)
        req = requests.get(endpoint, headers=self.headers)
        return json.loads(req.text)


    def get_solved_problems(self, institution_id, patient_id) -> Dict:
        endpoint = config.HCE_SOLVED_PROBLEMS.format(institutionId=institution_id, patientId=patient_id)
        req = requests.get(endpoint, headers=self.headers)
        return json.loads(req.text)

    ###############################################################################
    ## Institutions ###############################################################
    ###############################################################################

    def get_all_institutions(self):
        endpoint = config.ALL_INSTITUTIONS
        req = requests.get(endpoint, headers=self.headers)
        return json.loads(req.text)

    ###############################################################################
    ## Patient ####################################################################
    ###############################################################################

    def minimal_search(self, gender_id: int, id_number: int, id_type: int) -> List:
        endpoint = config.MINIMAL_SEARCH
        payload = {"genderId": gender_id, "identificationTypeId": id_type,
                   "identificationNumber": id_number}
        req = requests.get(endpoint, headers=self.headers, params=payload)
        return json.loads(req.text)


    def get_patient_complete_data(self, id_patient: int) -> Dict:
        endpoint = config.PATIENT_COMPLETE_DATA % id_patient
        req = requests.get(endpoint, headers=self.headers)
        return json.loads(req.text)

