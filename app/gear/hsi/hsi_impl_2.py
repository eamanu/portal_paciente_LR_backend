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