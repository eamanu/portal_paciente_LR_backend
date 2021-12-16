import os

# HSI - La Rioja
HSI_URL = "http://hsi.larioja.gob.ar:8080"
HSI_USERNAME = os.getenv("HSI_USERNAME")
HSI_PASSWORD = os.getenv("HSI_PASSWORD")
HSI_ORIGIN_HEADER = "portal_paciente_lr"

# endpoints
API_BASE = HSI_URL + "/api"
ALL_INSTITUTIONS = API_BASE + "/institution/all"
MINIMAL_SEARCH = API_BASE + "/person/minimalsearch"
PATIENT_COMPLETE_DATA = API_BASE + "/patient/%d/completedata"
HCE_VITAL_SIGNS = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/vitalSigns"
