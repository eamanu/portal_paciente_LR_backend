from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional


class SumarRow(BaseModel):
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


class SumarResult(BaseModel):
    sumar_rows: List[SumarRow]
