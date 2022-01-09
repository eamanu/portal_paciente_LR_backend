import os

###############################################################################
## HSI - La Rioja #############################################################
###############################################################################

HSI_URL = "http://hsi.larioja.gob.ar:8080"
HSI_USERNAME = os.getenv("HSI_USERNAME")
HSI_PASSWORD = os.getenv("HSI_PASSWORD")
HSI_ORIGIN_HEADER = "portal_paciente_lr"

# endpoints
API_BASE = HSI_URL + "/api"
ALL_INSTITUTIONS = API_BASE + "/institution/all"
ALL_IDENTIFICATION_TYPES = API_BASE + "/backoffice/identificationTypes/elements"
ALL_PROVINCES = API_BASE + "/backoffice/provinces/elements"
MINIMAL_SEARCH = API_BASE + "/person/minimalsearch"
PATIENT_BASIC_DATA = API_BASE + "/patient/%d/basicdata"
PATIENT_COMPLETE_DATA = API_BASE + "/patient/%d/completedata"
HCE_VITAL_SIGNS = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/vitalSigns"
HCE_SOLVED_PROBLEMS = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/solvedProblems"

