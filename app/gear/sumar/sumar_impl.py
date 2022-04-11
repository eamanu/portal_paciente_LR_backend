from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

from app.gear.log.main_logger import MainLogger, logging
from app.gear.sumar.database import engine
from app.gear.sumar.sql_sumar import SQL_SUMAR


@dataclass(order=True, frozen=True)
class Result:
    id_afiliado: int
    nombre: str
    tipo_doc: str
    dni: str
    clase_doc: str
    sexo: str
    fecha_nacimiento: Optional[date]
    fecha_comprobante: Optional[datetime]
    periodo: Optional[str]
    peso: Optional[float]
    tension_arterial: Optional[str]
    diagnostico: Optional[str]
    codigo: Optional[str]
    grupo: Optional[str]
    subgrupo: Optional[str]
    descripcion: Optional[str]
    dias_uti: Optional[int]
    dias_sala: Optional[int]
    dias_total: Optional[int]


logger = MainLogger()
module = logging.getLogger(__name__)


class SumarImpl:
    def __init__(self):
        self.engine = engine

    def get_data(self, dni_afiliado: str):
        sentence = SQL_SUMAR.format(dni_afiliado=dni_afiliado)
        logger.log_info_message(f"SQL to run, {sentence}", module)
        with self.engine.connect() as conn:
            exec_result = conn.execute(sentence)
            result = [Result(*row.values()) for row in exec_result]
        return result
