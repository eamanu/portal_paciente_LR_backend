import json
from typing import Dict

import requests

from app.hsi.config import HCE_VITAL_SIGNS
from app.hsi.hsi import HSIToken


class HCEGeneralState:
    def __init__(self):
        self.token = HSIToken().token
        self.hce_vital_sign = HCE_VITAL_SIGNS

    @property
    def headers(self):
        return {"accept": "*/*", "Authorization": self.token}

    def get_vital_signs(self, institution_id, patient_id) -> Dict:
        endpoint = self.hce_vital_sign.format(institutionId=institution_id, patientId=patient_id)
        req = requests.get(endpoint, headers=self.headers)
        return json.loads(req.text)