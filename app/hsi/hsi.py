import json
from typing import Dict

import requests

from app.config import HSI_PASSWORD, HSI_URL, HSI_USERNAME, HSI_ORIGIN_HEADER


class HSIToken:
    _instance = None
    token: str = ''
    refresh_token: str = ''
    url_auth: str = "/api/auth"
    hsi_url: str = HSI_URL
    username: str = HSI_USERNAME
    password: str = HSI_PASSWORD

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HSIToken, cls).__new__(cls)
        return cls._instance

    @property
    def url(self):
        return self.hsi_url + self.url_auth

    @property
    def data(self) -> str:
        data = {"username": self.username, "password": self.password}
        return json.dumps(data)

    @property
    def header(self) -> Dict:
        return {"Origin": HSI_ORIGIN_HEADER, "Content-Type": "application/json", "accept": "*/*"}

    def connect(self):
        req = json.loads(requests.post(self.url, data=self.data, headers=self.header).text)
        self.token = req['token']
        self.refresh_token = req['refreshToken']


class HCEGeneralState:
    def __init__(self):
        self.token = HSIToken().token
        self.base_url = HSI_URL
        self.endpoint = '/api/institutions/{institutionId}/patient/{patientId}/hce/general-state'

    @property
    def headers(self):
        return {"accept": "*/*", "Authorization": self.token}

    def get_vital_signs(self, institution_id, patient_id) -> Dict:
        final_endpoint = '/vitalSigns'
        url = self.base_url + self.endpoint.format(institutionId=institution_id, patientId=patient_id) + final_endpoint
        req = requests.get(url, headers=self.headers)
        return json.loads(req.text)
