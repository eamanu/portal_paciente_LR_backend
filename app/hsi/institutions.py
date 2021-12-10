import json
from typing import Dict

import requests

from app.hsi.config import ALL_INSTITUTIONS
from app.hsi.hsi import HSIToken


class HSIInstitutions:
    def __init__(self):
        self.token = HSIToken().connect().token
        self.endpoint = ALL_INSTITUTIONS

    @property
    def headers(self) -> Dict[str, str]:
        return {"accept": "*/*", "Authorization": self.token}

    def get_all_institutions(self):
        req = requests.get(self.endpoint, headers=self.headers)
        return json.loads(req.text)
