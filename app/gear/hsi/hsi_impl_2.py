import pprint

from app.gear.log.main_logger import MainLogger, logging
from app.gear.hsi.database import engine

logger = MainLogger()
module = logging.getLogger(__name__)

DONT_ALLOWS_VERBS = ("DELETE", "INSERT", "UPDATE", "CREATE", "ALTER")


class HSIImpl2:
    def __init__(self):
        self.engine = engine

    def execute(self, sql: str):
        """Execute wherever you want"""
        logger.log_info_message(f"SQL to run, {sql}", module)
        for verb in DONT_ALLOWS_VERBS:
            if verb in sql:
                logger.log_info_message(f"Here there's Macri locked up....", module)
                return False
        with self.engine.connect() as conn:
            exec_result = conn.execute(sql)
        return [row for row in exec_result]

    def get_allergies(self, institution_id: int, patient_id: int):

        '''
        [
          {
            "id": 0,
            "statusId": "string",
            "snomed": {
              "id": 0,
              "sctid": "string",
              "pt": "string",
              "parentId": "string",
              "parentFsn": "string"
            },
            "categoryId": 0,
            "criticalityId": 0
          }
        ]
        '''

        data = []

        results = self.execute("""  SELECT ai.id,
             ai.patient_id,
             ai.status_id AS statusId,
             ai.category_id AS categoryId,
             ai.criticality AS criticalityId,
             s.id AS snomed_id,
             s.sctid AS snomed_sctid,
             s.pt AS snomed_pt,
             s.parent_id AS snomed_parentId,
             s.parent_fsn AS snomed_parentFsn
        FROM allergy_intolerance ai INNER JOIN patient p ON p.id = ai.patient_id
                                    INNER JOIN snomed s ON s.id = ai.snomed_id
                                    INNER JOIN person per ON per.id = p.person_id
       WHERE 1 = 1
         AND ai.patient_id IN (""" + str(patient_id) + """)""")

        if len(results) > 0:
            for r in results:
                data.append({ "id": r["id"],
                              "patient_id": r["patient_id"],
                              "statusId": r["statusid"],
                              "categoryId": r["categoryid"],
                              "criticalityId": r["criticalityid"],
                              "snomed": {"id": r["snomed_id"],
                                         "sctid": r["snomed_sctid"],
                                         "pt": r["snomed_pt"],
                                         "parentId": r["snomed_parentid"],
                                         "parentFsn": r["snomed_parentfsn"]}})


        return data


    def get_anthropometric_data(self, institution_id: int, patient_id: int):

        '''
        {
            "bloodType": {
                "id": 0,
                "value": "string",
                "effectiveTime": "string"
            },
            "height": {
                "id": 0,
                "value": "string",
                "effectiveTime": "string"
            },
            "weight": {
                "id": 0,
                "value": "string",
                "effectiveTime": "string"
            },
            "bmi": {
                "id": 0,
                "value": "string",
                "effectiveTime": "string"
            },
            "headCircumference": {
                "id": 0,
                "value": "string",
                "effectiveTime": "string"
            }
        }
        '''

        data = []

        results = self.execute("""  SELECT ol.id AS bloodType_id,
         ol.value AS bloodType_value,
         ol.effective_time AS bloodType_effectiveTime
    FROM observation_lab ol INNER JOIN patient p ON p.id = ol.patient_id
                            INNER JOIN snomed s ON s.id = ol.snomed_id
                            INNER JOIN person per ON per.id = p.person_id
   WHERE 1 = 1
     AND s.id = 11
     AND ol.patient_id IN (""" + str(patient_id) + """)
ORDER BY ol.effective_time DESC
   LIMIT 1""")

        if len(results) > 0:
            for r in results:
                data.append({ "bloodType": {"id": r["bloodtype_id"],
                                            "value": r["bloodtype_value"],
                                            "effectiveTime": r["bloodtype_effectivetime"]}})

        results = self.execute("""  SELECT ovs.id AS height_id,
         ovs.value AS height_value,
         ovs.effective_time AS height_effectiveTime
    FROM observation_vital_sign ovs INNER JOIN patient p ON p.id = ovs.patient_id
                                    INNER JOIN snomed s ON s.id = ovs.snomed_id
                                    INNER JOIN person per ON per.id = p.person_id
   WHERE 1 = 1
     AND s.id = 8
     AND ovs.patient_id IN (""" + str(patient_id) + """)
ORDER BY ovs.effective_time DESC
   LIMIT 1""")

        if len(results) > 0:
            for r in results:
                data.append({"height": {"id": r["height_id"],
                                        "value": r["height_value"],
                                        "effectiveTime": r["height_effectivetime"]}})

        results = self.execute("""  SELECT ovs.id AS weight_id,
         ovs.value AS weight_value,
         ovs.effective_time AS weight_effectiveTime
    FROM observation_vital_sign ovs INNER JOIN patient p ON p.id = ovs.patient_id
                                    INNER JOIN snomed s ON s.id = ovs.snomed_id
                                    INNER JOIN person per ON per.id = p.person_id
   WHERE 1 = 1
     AND s.id = 9
     AND ovs.patient_id IN (""" + str(patient_id) + """)
ORDER BY ovs.effective_time DESC
   LIMIT 1""")

        if len(results) > 0:
            for r in results:
                data.append({"weight": {"id": r["weight_id"],
                                        "value": r["weight_value"],
                                        "effectiveTime": r["weight_effectivetime"]}})

        results = self.execute("""  SELECT ovs.id AS bmi_id,
         ovs.value AS bmi_value,
         ovs.effective_time AS bmi_effectiveTime
    FROM observation_vital_sign ovs INNER JOIN patient p ON p.id = ovs.patient_id
                                    INNER JOIN snomed s ON s.id = ovs.snomed_id
                                    INNER JOIN person per ON per.id = p.person_id
   WHERE 1 = 1
     AND s.id = 10
     AND ovs.patient_id IN (""" + str(patient_id) + """)
ORDER BY ovs.effective_time DESC
   LIMIT 1""")

        if len(results) > 0:
            for r in results:
                data.append({"bmi": {"id": r["bmi_id"],
                                     "value": r["bmi_value"],
                                     "effectiveTime": r["bmi_effectivetime"]}})

        results = self.execute("""  SELECT ovs.id AS headCircumference_id,
         ovs.value AS headCircumference_value,
         ovs.effective_time AS headCircumference_effectiveTime
    FROM observation_vital_sign ovs INNER JOIN patient p ON p.id = ovs.patient_id
                                    INNER JOIN snomed s ON s.id = ovs.snomed_id
                                    INNER JOIN person per ON per.id = p.person_id
   WHERE 1 = 1
     AND s.id = 1409
     AND ovs.patient_id IN (""" + str(patient_id) + """)
ORDER BY ovs.effective_time DESC
   LIMIT 1""")

        if len(results) > 0:
            for r in results:
                data.append({"headCircumference": {"id": r["headcircumference_id"],
                                                   "value": r["headcircumference_value"],
                                                   "effectiveTime": r["headcircumference_effectivetime"]}})

        return data

    def get_chronic(self, institution_id: int, patient_id: int):

        '''
        [
          {
            "id": 0,
            "statusId": "string",
            "snomed": {
              "id": 0,
              "sctid": "string",
              "pt": "string",
              "parentId": "string",
              "parentFsn": "string"
            },
            "startDate": "string",
            "inactivationDate": "string",
            "severity": "string",
            "hasPendingReference": true
          }
        ]
        '''

        data = []

        results = self.execute("""  SELECT hc.id,
         hc.patient_id,
         hc.status_id AS statusId,
         hc.start_date AS startDate,
         hc.inactivation_date AS inactivationDate,
         hc.severity,
         NULL AS hasPendingReference,
         s.id AS snomed_id,
         s.sctid AS snomed_sctid,
         s.pt AS snomed_pt,
         s.parent_id AS snomed_parentId,
         s.parent_fsn AS snomed_parentFsn
    FROM health_condition hc INNER JOIN patient p ON p.id = hc.patient_id
                             INNER JOIN snomed s ON s.id = hc.snomed_id
                             INNER JOIN person per ON per.id = p.person_id
   WHERE 1 = 1
     AND hc.problem_id = '-55607006'
     AND hc.patient_id IN (""" + str(patient_id) + """)
ORDER BY hc.start_date DESC""")

        if len(results) > 0:
            for r in results:
                data.append({ "id": r["id"],
                              "patient_id": r["patient_id"],
                              "statusId": r["statusid"],
                              "startDate": r["startdate"],
                              "inactivationDate": r["inactivationdate"],
                              "severity": r["severity"],
                              "hasPendingReference": r["haspendingreference"],
                              "snomed": {"id": r["snomed_id"],
                                         "sctid": r["snomed_sctid"],
                                         "pt": r["snomed_pt"],
                                         "parentId": r["snomed_parentid"],
                                         "parentFsn": r["snomed_parentfsn"]}})


        return data

    def get_immunizations(self, institution_id: int, patient_id: int):

        '''
        [
          {
            "id": 0,
            "statusId": "string",
            "snomed": {
              "id": 0,
              "sctid": "string",
              "pt": "string",
              "parentId": "string",
              "parentFsn": "string"
            },
            "administrationDate": "string",
            "note": "string",
            "institution": {
              "id": 0,
              "name": "string",
              "sisaCode": "string"
            },
            "dose": {
              "description": "string",
              "order": 0
            },
            "condition": {
              "id": 0,
              "description": "string"
            },
            "scheme": {
              "id": 0,
              "description": "string"
            },
            "lotNumber": "string",
            "doctor": {
              "id": 0,
              "licenceNumber": "string",
              "firstName": "string",
              "lastName": "string",
              "identificationNumber": "string",
              "phoneNumber": "string",
              "clinicalSpecialties": [
                {
                  "id": 0,
                  "name": "string"
                }
              ]
            }
          }
        ]
        '''

        data = []

        results = self.execute("""  SELECT i.id,
         i.patient_id,
         i.status_id AS statusId,
         i.administration_date AS administrationDate,
         n.description as note,
         i.institution_info AS institution,
         i.dose AS dose_description,
         i.dose_order AS dose_order,
         i.condition_id AS condition_id,
         '' AS condition_description,
         NULL AS scheme_id,
         NULL AS scheme_description,
         i.lot_number AS lotNumber,
         i.doctor_info AS doctor,
         s.id AS snomed_id,
         s.sctid AS snomed_sctid,
         s.pt AS snomed_pt,
         s.parent_id AS snomed_parentId,
         s.parent_fsn AS snomed_parentFsn
    FROM inmunization i INNER JOIN patient p ON p.id = i.patient_id
                        INNER JOIN note n on n.id = i.note_id
                        INNER JOIN snomed s ON s.id = i.snomed_id
                        INNER JOIN person per ON per.id = p.person_id
   WHERE 1 = 1
     AND i.patient_id IN (""" + str(patient_id) + """)""")

        if len(results) > 0:
            for r in results:
                data.append({ "id": r["id"],
                              "patient_id": r["patient_id"],
                              "statusId": r["statusid"],
                              "administrationDate": r["administrationdate"],
                              "note": r["note"],
                              "institution": { "id": "NULL",
                                               "name": r["institution"],
                                               "sisaCode": "NULL" },
                              "dose": { "description": r["dose_description"],
                                        "order": r["dose_order"] },
                              "condition": {"id": r["condition_id"],
                                            "description": r["condition_description"] },
                              "scheme": { "id": r["scheme_id"],
                                          "description": r["scheme_description"] },
                              "lotNumber": r["lotnumber"],
                              "doctor": { "id": "NULL",
                                          "name": r["doctor"]},
                                          "licenceNumber": "NULL",
                                          "firstName": "NULL",
                                          "lastName": "NULL",
                                          "identificationNumber": "NULL",
                                          "phoneNumber": "NULL",
                                          "clinicalSpecialties": [],
                              "snomed": {"id": r["snomed_id"],
                                         "sctid": r["snomed_sctid"],
                                         "pt": r["snomed_pt"],
                                         "parentId": r["snomed_parentid"],
                                         "parentFsn": r["snomed_parentfsn"]}})


        return data


    def get_medications(self, institution_id: int, patient_id: int):

        '''
        [
          {
            "id": 0,
            "statusId": "string",
            "snomed": {
              "id": 0,
              "sctid": "string",
              "pt": "string",
              "parentId": "string",
              "parentFsn": "string"
            },
            "suspended": true
          }
        ]
        '''

        data = []

        results = self.execute("""  SELECT ms.id,
         ms.patient_id,
         ms.status_id AS statusId,
         (CASE WHEN ms.status_id = '385655000' THEN true ELSE false END) AS suspended,
         s.id AS snomed_id,
         s.sctid AS snomed_sctid,
         s.pt AS snomed_pt,
         s.parent_id AS snomed_parentId,
         s.parent_fsn AS snomed_parentFsn
    FROM medication_statement ms INNER JOIN patient p ON p.id = ms.patient_id
                                 INNER JOIN snomed s ON s.id = ms.snomed_id
                                 INNER JOIN person per ON per.id = p.person_id
   WHERE 1 = 1
     AND ms.patient_id IN (""" + str(patient_id) + """)""")

        if len(results) > 0:
            for r in results:
                data.append({ "id": r["id"],
                              "patient_id": r["patient_id"],
                              "statusId": r["statusid"],
                              "suspended": r["suspended"],
                              "snomed": {"id": r["snomed_id"],
                                         "sctid": r["snomed_sctid"],
                                         "pt": r["snomed_pt"],
                                         "parentId": r["snomed_parentid"],
                                         "parentFsn": r["snomed_parentfsn"]}})


        return data


    def get_tooth_records(self, institution_id: int, patient_id: int, tooth_sct_id: str):

        '''
        [
          {
            "snomed": {
              "id": 0,
              "sctid": "string",
              "pt": "string",
              "parentId": "string",
              "parentFsn": "string"
            },
            "surfaceSctid": "string",
            "date": {
              "year": 0,
              "month": 0,
              "day": 0
            }
          }
        ]
        '''

        data = []

        results = self.execute("""  SELECT op.id,
         op.patient_id,
         op.surface_id AS surfaceSctid,
         op.performed_date AS date,
         s.id AS snomed_id,
         s.sctid AS snomed_sctid,
         s.pt AS snomed_pt,
         s.parent_id AS snomed_parentId,
         s.parent_fsn AS snomed_parentFsn
    FROM odontology_procedure op INNER JOIN patient p ON p.id = op.patient_id
                                 INNER JOIN snomed s ON s.id = op.snomed_id
                                 INNER JOIN person per ON per.id = p.person_id
   WHERE 1 = 1
     AND op.patient_id IN (""" + str(patient_id) + """)
     AND s.sctid = '""" + tooth_sct_id + """'""")

        if len(results) > 0:
            for r in results:
                data.append({ "id": r["id"],
                              "patient_id": r["patient_id"],
                              "surfaceSctid": r["surfacesctid"],
                              "snomed": {"id": r["snomed_id"],
                                         "sctid": r["snomed_sctid"],
                                         "pt": r["snomed_pt"],
                                         "parentId": r["snomed_parentid"],
                                         "parentFsn": r["snomed_parentfsn"]},
                              "date": {"year": r["date"].year,
                                       "month": r["date"].month,
                                       "day": r["date"].day}})


        return data


    def get_active_problems(self, institution_id: int, patient_id: int):

        '''
        [
          {
            "id": 0,
            "statusId": "string",
            "snomed": {
              "id": 0,
              "sctid": "string",
              "pt": "string",
              "parentId": "string",
              "parentFsn": "string"
            },
            "startDate": "string",
            "inactivationDate": "string",
            "severity": "string",
            "hasPendingReference": true
          }
        ]
        '''

        data = []

        results = self.execute("""  SELECT hc.id,
         hc.patient_id,
         hc.status_id AS statusId,
         hc.start_date AS startDate,
         hc.inactivation_date AS inactivationDate,
         hc.severity,
         false AS hasPendingReference,
         s.id AS snomed_id,
         s.sctid AS snomed_sctid,
         s.pt AS snomed_pt,
         s.parent_id AS snomed_parentId,
         s.parent_fsn AS snomed_parentFsn
    FROM health_condition hc INNER JOIN patient p ON p.id = hc.patient_id
                             INNER JOIN snomed s ON s.id = hc.snomed_id
                             INNER JOIN person per ON per.id = p.person_id
   WHERE 1 = 1
     AND hc.status_id IN ('55561003')
     AND hc.patient_id IN (""" + str(patient_id) + """)""")

        if len(results) > 0:
            for r in results:
                data.append({ "id": r["id"],
                              "patient_id": r["patient_id"],
                              "statusId": r["statusid"],
                              "startDate": r["startdate"],
                              "inactivationDate": r["inactivationdate"],
                              "severity": r["severity"],
                              "hasPendingReference": r["haspendingreference"],
                              "snomed": {"id": r["snomed_id"],
                                         "sctid": r["snomed_sctid"],
                                         "pt": r["snomed_pt"],
                                         "parentId": r["snomed_parentid"],
                                         "parentFsn": r["snomed_parentfsn"]}})


        return data


    def get_solved_problems(self, institution_id: int, patient_id: int):

        '''
        [
          {
            "id": 0,
            "statusId": "string",
            "snomed": {
              "id": 0,
              "sctid": "string",
              "pt": "string",
              "parentId": "string",
              "parentFsn": "string"
            },
            "startDate": "string",
            "inactivationDate": "string",
            "severity": "string",
            "hasPendingReference": true
          }
        ]
        '''

        data = []

        results = self.execute("""  SELECT hc.id,
         hc.patient_id,
         hc.status_id AS statusId,
         hc.start_date AS startDate,
         hc.inactivation_date AS inactivationDate,
         hc.severity,
         false AS hasPendingReference,
         s.id AS snomed_id,
         s.sctid AS snomed_sctid,
         s.pt AS snomed_pt,
         s.parent_id AS snomed_parentId,
         s.parent_fsn AS snomed_parentFsn
    FROM health_condition hc INNER JOIN patient p ON p.id = hc.patient_id
                             INNER JOIN snomed s ON s.id = hc.snomed_id
                             INNER JOIN person per ON per.id = p.person_id
   WHERE 1 = 1
     AND hc.status_id IN ('723506003', '277022003')
     AND hc.patient_id IN (""" + str(patient_id) + """)""")

        if len(results) > 0:
            for r in results:
                data.append({ "id": r["id"],
                              "patient_id": r["patient_id"],
                              "statusId": r["statusid"],
                              "startDate": r["startdate"],
                              "inactivationDate": r["inactivationdate"],
                              "severity": r["severity"],
                              "hasPendingReference": r["haspendingreference"],
                              "snomed": {"id": r["snomed_id"],
                                         "sctid": r["snomed_sctid"],
                                         "pt": r["snomed_pt"],
                                         "parentId": r["snomed_parentid"],
                                         "parentFsn": r["snomed_parentfsn"]}})


        return data

    def get_vital_signs(self, institution_id: int, patient_id: int):

        '''
        [
          {
            "id": 0,
            "snomed": {
              "id": 0,
              "sctid": "string",
              "pt": "string",
              "parentId": "string",
              "parentFsn": "string"
            },
            "value": "string",
            "loinc_code": "string"
          }
        ]
        '''

        data = []

        results = self.execute("""  SELECT ovs.id,
         ovs.patient_id,
         ovs.value,
         ovs.loinc_code,
         s.id AS snomed_id,
         s.sctid AS snomed_sctid,
         s.pt AS snomed_pt,
         s.parent_id AS snomed_parentId,
         s.parent_fsn AS snomed_parentFsn
    FROM observation_vital_sign ovs INNER JOIN patient p ON p.id = ovs.patient_id
                                    INNER JOIN snomed s ON s.id = ovs.snomed_id
                                    INNER JOIN person per ON per.id = p.person_id
   WHERE 1 = 1
     AND ovs.patient_id IN (""" + str(patient_id) + """)""")

        if len(results) > 0:
            for r in results:
                data.append({ "id": r["id"],
                              "patient_id": r["patient_id"],
                              "loinc_code": r["loinc_code"],
                              "value": r["value"],
                              "snomed": {"id": r["snomed_id"],
                                         "sctid": r["snomed_sctid"],
                                         "pt": r["snomed_pt"],
                                         "parentId": r["snomed_parentid"],
                                         "parentFsn": r["snomed_parentfsn"]}})


        return data
