import enum

class PersonStatusEnum(enum.Enum):
    validation_pending = 1
    validated = 2
    validation_rejected = 3
