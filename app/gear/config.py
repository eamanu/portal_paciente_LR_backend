import os

# region HSI - La Rioja

HSI_URL = "http://hsi.larioja.gob.ar:8080"
HSI_USERNAME = os.getenv("HSI_USERNAME")
HSI_PASSWORD = os.getenv("HSI_PASSWORD")
HSI_ORIGIN_HEADER = "portal_paciente_lr"

# endregion

# region HSI end points

API_BASE = HSI_URL + "/api"
ALL_INSTITUTIONS = API_BASE + "/institution/all"
ALL_IDENTIFICATION_TYPES = API_BASE + "/backoffice/identificationTypes/elements"
ALL_PROVINCES = API_BASE + "/backoffice/provinces/elements"
MINIMAL_SEARCH = API_BASE + "/person/minimalsearch"
PATIENT_BASIC_DATA = API_BASE + "/patient/%d/basicdata"
PATIENT_COMPLETE_DATA = API_BASE + "/patient/%d/completedata"
HCE_ALLERGIES = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/allergies"
HCE_ANTHROPOMETRIC_DATA = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/allergies"
HCE_CHRONIC_DATA = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/chronic"
HCE_FAMILY_HISTORIES = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/familyHistories"
HCE_HOSPITALIZATION = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/hospitalization"
HCE_IMMUNIZATIONS = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/immunizations"
HCE_MEDICATIONS = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/medications"
HCE_PERSONAL_HISTORIES = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/personalHistories"
HCE_TOOTH_RECORDS = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/toothRecords/tooth/{toothSctid}"
HCE_ACTIVE_PROBLEMS = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/activeProblems"
HCE_VITAL_SIGNS = API_BASE + "/institutions/{institutionId}/patient/{patientId}/hce/general-state/vitalSigns"

# endregion

