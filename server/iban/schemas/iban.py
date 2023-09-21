from typing import Any, Optional

from pydantic import BaseModel

from server.core.enums import ValidationStatus


class BaseIban(BaseModel):
    iban: str


class ValidateIbanSchema(BaseIban):
    country: Optional[str]


class CreateIbanCheck(BaseIban):
    status: ValidationStatus


class UpdateIbanCheck(BaseIban):
    status: ValidationStatus


class BaseValidationResponse(BaseModel):
    status: ValidationStatus


class IbanValidationResponse(BaseValidationResponse):
    iban: str
    suggested_iban: Optional[str]
    created_at: Any

    class Config:
        orm_mode = True


class IbanPartialValidationResponse(BaseValidationResponse):
    pass
