import requests_mock

from app.gear.hsi.hsi_token import HSIToken
from app.gear.hsi import HSIPersons


def test_headers(mocker):
    mocker.patch.object(HSIToken, 'token')
    expected_header = {"accept": "*/*", "Authorization": "token"}
    person = HSIPersons()
    person.token = "token"
    assert expected_header == person.headers


def test_minimal_search():
    person = HSIPersons()
    person.token = "token"

    ids = '[1]'
    expected_ids = [1]
    endpoint = "http://hsi.larioja.gob.ar:8080/api/person/minimalsearch?genderId=2&identificationTypeId=1&identificationNumber=111111"  # NOQA
    with requests_mock.Mocker() as m:
        m.get(endpoint, text=ids)
        assert person.minimal_search(2, 111111, 1) == expected_ids


def test_get_patient_complete_data():
    person = HSIPersons()
    person.token = "token"

    endpoint = "http://hsi.larioja.gob.ar:8080/api/patient/1/completedata"
    complete_data = '{"name": "name", "surname": "surname", "id": "1"}'
    expected_complete_data = {"name": "name", "surname": "surname", "id": "1"}
    with requests_mock.Mocker() as m:
        m.get(endpoint, text=complete_data)
        assert person.get_patient_complete_data(1) == expected_complete_data