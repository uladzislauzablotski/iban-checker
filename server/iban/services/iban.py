import re
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from server.core.crud import IbanDbService
from server.core.enums import ValidationStatus
from server.iban.schemas import (CreateIbanCheck,
                                 IbanPartialValidationResponse,
                                 IbanValidationResponse, ValidateIbanSchema)


class BaseIbanService:
    pass


class MontenegroIbanService(BaseIbanService):
    @staticmethod
    async def is_valid_partial_iban(partial_iban: str) -> bool:
        # Remove spaces and convert to uppercase
        partial_iban = partial_iban.replace(' ', '').upper()

        # Check if the IBAN has the correct length for Montenegro
        if len(partial_iban) > 22:
            return False

        # Check if the country code and check digits are valid
        if not partial_iban.startswith('ME'):
            return False

        # Check if the rest of the IBAN is numeric
        if not partial_iban[2:].isdigit():
            return False

        return True

    @staticmethod
    async def is_valid(iban: str) -> bool:
        # Remove spaces and convert to uppercase
        iban = iban.replace(' ', '').upper()

        # Check if the IBAN has the correct length for Montenegro
        if len(iban) != 22:
            return False

        # Check if the country code and check digits are valid
        if not re.match(r'^ME\d{2}\d{3}\d{15}$', iban):
            return False

        # Rearrange IBAN to create a new string for checksum calculation
        rearranged_iban = iban[4:] + iban[:4]

        # Replace letters with corresponding numbers
        numeric_iban = ''
        for char in rearranged_iban:
            if char.isdigit():
                numeric_iban += char
            else:
                numeric_iban += str(ord(char) - ord('A') + 10)

        # Perform modulo operation to calculate the checksum
        remainder = int(numeric_iban) % 97

        # Check if the remainder is 1 (valid IBAN)
        return remainder == 1

    async def suggest_correct_iban(self, invalid_iban: str) -> Optional[str]:
        # TODO: need to improve the algo
        invalid_iban = invalid_iban.replace(' ', '').upper()

        # Check if the IBAN has the correct length for Montenegro
        if len(invalid_iban) > 22:
            invalid_iban = invalid_iban[:22]

        if len(invalid_iban) != 22:
            return None

        # Check if the country code and check digits are valid
        if not invalid_iban[2:].isdigit():
            return None

        suggested_iban = 'ME25' + invalid_iban[4:]

        return suggested_iban if await self.is_valid(iban=suggested_iban) else None


class IbanController:

    @staticmethod
    async def validate_iban(
        payload: ValidateIbanSchema,
        session: AsyncSession,
    ) -> IbanValidationResponse:
        """
        Check if provided iban is valid and return result of validation
        need to create validation check as a history in db
        """
        iban_service = MontenegroIbanService()  # hardcoded to montenegro
        is_valid = await iban_service.is_valid(iban=payload.iban)
        status = ValidationStatus.VALID if is_valid else ValidationStatus.NOT_VALID

        iban_check = await IbanDbService.create(
            input_data=CreateIbanCheck(iban=payload.iban, status=status),
            session=session
        )
        response = IbanValidationResponse.from_orm(iban_check)
        response.suggested_iban = await iban_service.suggest_correct_iban(
            invalid_iban=payload.iban) if not is_valid else None

        return response

    @staticmethod
    async def validate_partial_iban(payload: ValidateIbanSchema) -> IbanPartialValidationResponse:
        iban_service = MontenegroIbanService  # hardcoded to montenegro
        is_valid = await iban_service.is_valid_partial_iban(partial_iban=payload.iban)

        return IbanPartialValidationResponse(
            status=ValidationStatus.VALID if is_valid else ValidationStatus.NOT_VALID
        )
