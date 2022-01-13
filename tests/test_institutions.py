import requests_mock

from app.gear.hsi.hsi_token import HSIToken
from app.gear.hsi import HSIInstitutions


def test_headers(mocker):
    mocker.patch.object(HSIToken, 'token')
    expected_header = {"accept": "*/*", "Authorization": "token"}
    hsi_institution = HSIInstitutions()
    hsi_institution.token = "token"
    assert expected_header == hsi_institution.headers


def test_get_all_institutions():
    hsi_institution = HSIInstitutions()
    hsi_institution.token = "token"

    institutions = '[{"id":"1", "name": "inst1"}, ' \
                   '{"id": "2", "name": "inst2"}]'
    expected_institutions = [{"id": "1", "name": "inst1"},
                             {"id": "2", "name": "inst2"}]
    endpoint = "http://hsi.larioja.gob.ar:8080/api/institution/all"

    with requests_mock.Mocker() as m:
        m.get(endpoint, text=institutions)
        assert hsi_institution.get_all_institutions() == expected_institutions
