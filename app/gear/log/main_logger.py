import logging
from app.config.config import LOG_FORMAT, LOG_PATH

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(LOG_FORMAT)

file_handler = logging.FileHandler(LOG_PATH)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class MainLogger(metaclass=Singleton):

    def log_message(self, message:str, logger=None):
        logger.addHandler(file_handler)

        if logger.getEffectiveLevel() == logging.INFO or logger.getEffectiveLevel() == logging.NOTSET:
            logger.info(message)

        if logger.getEffectiveLevel() == logging.WARNING:
            logger.warning(message)

        if logger.getEffectiveLevel() == logging.ERROR:
            logger.error(message)

        if logger.getEffectiveLevel() == logging.CRITICAL:
            logger.critical(message)

    def log_info_message(self, message:str, logger=None):
        logger.setLevel(logging.INFO)
        self.log_message(message, logger)

    def log_warning_message(self, message:str, logger=None):
        logger.setLevel(logging.WARNING)
        self.log_message(message, logger)

    def log_error_message(self, message:str, logger=None):
        logger.setLevel(logging.ERROR)
        self.log_message(message, logger)

    def log_critical_message(self, message:str, logger=None):
        logger.setLevel(logging.CRITICAL)
        self.log_message(message, logger)

