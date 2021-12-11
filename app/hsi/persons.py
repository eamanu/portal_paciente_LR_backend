import json
from typing import List, Dict

import requests

from app.hsi.config import MINIMAL_SEARCH, PATIENT_COMPLETE_DATA
from app.hsi.hsi import HSIToken


class HSIPersons:
    def __init__(self):
        self.token = HSIToken().connect().token
        self.minimal_search_endpoint = MINIMAL_SEARCH
        self.complete_data_endpoint = PATIENT_COMPLETE_DATA

    @property
    def headers(self) -> Dict[str, str]:
        return {"accept": "*/*", "Authorization": self.token}

    def minimal_search(self, gender_id: int, id_number: int, id_type: int) -> List:
        payload = {"genderId": gender_id, "identificationTypeId": id_type,
                   "identificationNumber": id_number}
        req = requests.get(self.minimal_search_endpoint, headers=self.headers, params=payload)
        return json.loads(req.text)

    def get_patient_complete_data(self, id_patient: int) -> Dict:
        endpoint = self.complete_data_endpoint % id_patient
        req = requests.get(endpoint, headers=self.headers)
        return json.loads(req.text)
