from app.gear.sumar.sumar_impl import SumarImpl
from app.schemas.sumar_result import SumarRow, SumarResult
from dataclasses import asdict


def get_afiliado_data(dni_afiliado: str) -> SumarResult:
    sumar = SumarImpl()
    data = sumar.get_data(dni_afiliado)
    rows = [SumarRow(**asdict(result)) for result in data]
    return SumarResult(sumar_rows=rows)
