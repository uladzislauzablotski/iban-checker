from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.core.database import get_session
from server.iban.schemas import (IbanPartialValidationResponse,
                                 IbanValidationResponse, ValidateIbanSchema)
from server.iban.services import IbanController

router = APIRouter(prefix="/iban")
controller = IbanController()


@router.post("/validate", response_model=IbanValidationResponse)
async def validate_iban(
    payload: ValidateIbanSchema,
    session: AsyncSession = Depends(get_session)
):
    """
    Validate iban. For now Montenegro ibans supported only
    """
    return await controller.validate_iban(payload=payload, session=session)


@router.post("/validate_partial", response_model=IbanPartialValidationResponse)
async def validate_partial_iban(payload: ValidateIbanSchema):
    """Validate partial iban provided (ex. when searching)"""
    return await controller.validate_partial_iban(payload)
