import requests_mock

from app.gear.hsi import HCEGeneralState
from app.gear.hsi.hsi_token import HSIToken


def test_headers(mocker):
    mocker.patch.object(HSIToken, 'token')
    expected_header = {"accept": "*/*", "Authorization": "token"}
    hce_general_state = HCEGeneralState()
    hce_general_state.token = "token"
    assert expected_header == hce_general_state.headers


def test_get_all_institutions():
    hce_general_state = HCEGeneralState()
    hce_general_state.token = "token"

    vital_sign = '{"test": "test"}'
    expected_institutions = {"test": "test"}
    endpoint = "http://hsi.larioja.gob.ar:8080/api/institutions/1/patient/1/hce/general-state"

    with requests_mock.Mocker() as m:
        m.get(endpoint, text=vital_sign)
        assert hce_general_state.get_vital_signs(1, 1) == expected_institutions
