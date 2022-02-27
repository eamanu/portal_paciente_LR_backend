import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from app.gear.log.main_logger import MainLogger, logging

from jose import jwt

from app.config.config import SECRET_KEY, ALGORITHM


@dataclass
class BearerToken:
    bearer_token: str
    pattern_bearer: str = '(Bearer )(.*)'

    log = MainLogger()
    module = logging.getLogger(__name__)

    @property
    def token(self) -> str:
        token_match = re.search(self.pattern_bearer, self.bearer_token)
        if token_match is None:
            return ''
        return token_match.group(2)

    @property
    def payload(self) -> Optional[Dict]:
        try:
            return jwt.decode(self.token, SECRET_KEY, algorithms=[ALGORITHM])
        except Exception as e:
            self.log.log_error_message(e, self.module)
            return None

    @property
    def is_expired(self) -> bool:
        expires = datetime.fromtimestamp(self.payload.get("exp"))
        return expires < datetime.now()
