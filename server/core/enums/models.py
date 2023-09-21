from .base_enum import BaseEnum


class ValidationStatus(str, BaseEnum):
    VALID = "Valid"
    NOT_VALID = "Not valid"


class StatusEnum(str, BaseEnum):
    success = "Success"
    failure = "Failure"
