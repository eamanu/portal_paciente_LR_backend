import json
from typing import Dict

import requests
from app.hsi.config import MINIMAL_SEARCH
from app.hsi.hsi import HSIToken


class HSIPersons:
    def __init__(self):
        self.token = HSIToken().connect().token
        self.minimal_search_endpoint = MINIMAL_SEARCH

    @property
    def headers(self) -> Dict[str, str]:
        return {"accept": "*/*", "Authorization": self.token}

    def minimal_search(self, gender_id: int, id_number: int, id_type: int) -> Dict:
        payload = {"genderId": gender_id, "identificationTypeId": id_type,
                   "identificationNumber": id_number}

        req = requests.get(self.minimal_search_endpoint, headers=self.headers, params=payload)
        return json.loads(req.text)
