from app.gear.local.sumar import get_afiliado_data
from app.routes.common import router_sumar
from app.schemas.sumar_result import SumarResult


@router_sumar.get("/data/{dni_afiliado}", tags=["SUMAR", "data"], response_model=SumarResult)
async def get_sumar_data(dni_afiliado: str) -> SumarResult:
    return get_afiliado_data(dni_afiliado)
