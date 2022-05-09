import enum

class PersonStatusEnum(enum.Enum):
    email_validation_pending = 1
    email_validated = 2
    email_validation_rejected = 3
