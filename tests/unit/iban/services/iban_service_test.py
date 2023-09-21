import pytest
from datetime import datetime
from unittest.mock import patch

from server.iban.services import IbanController, MontenegroIbanService
from server.iban.schemas import ValidateIbanSchema
from server.core.enums import ValidationStatus
from server.core.crud import IbanDbService
from server.core.models import IbanModel


class TestIbanService:

    @pytest.mark.parametrize(
        "iban,expected",
        [
            ("ME25505000012345678951", True),
            ("LE25505000012345678951", False),
            ("LE25505000022345678951", False)
        ]
    )
    @pytest.mark.asyncio
    async def test_is_valid(self, iban, expected):
        result = await MontenegroIbanService.is_valid(iban=iban)
        assert result == expected

    @pytest.mark.parametrize(
        "iban,expected",
        [
            ("ME05505000", True),
            ("LEF5505000012345678951", False),
            ("LE05505000000000000000000000000000", False),
        ]
    )
    @pytest.mark.asyncio
    async def test_is_valid_partial_iban(self, iban, expected):
        result = await MontenegroIbanService.is_valid_partial_iban(partial_iban=iban)
        assert result == expected

    @pytest.mark.parametrize(
        "iban,expected",
        [
            ("ME2550500001234567895100", "ME25505000012345678951"),
            ("LE2550500001234567895100", "ME25505000012345678951"),
            ("ME25505000012345638951", None),
            ("LE255050wer1234567895100", None)
        ]
    )
    @pytest.mark.asyncio
    async def test_suggest_correct_iban(self, iban, expected):
        result = await MontenegroIbanService().suggest_correct_iban(invalid_iban=iban)
        assert result == expected


class TestIbanController:

    @pytest.mark.parametrize(
        "iban,status",
        [
            ("ME25505000012345678951", ValidationStatus.VALID),
            ("LE25505000012345678951", ValidationStatus.NOT_VALID),
            ("LE25505000022345678951", ValidationStatus.NOT_VALID)
        ]
    )
    @patch.object(IbanDbService, "create")
    @pytest.mark.asyncio
    async def test_is_valid(self, create_mock, iban, status):
        payload = ValidateIbanSchema(iban=iban)
        create_mock.return_value = IbanModel(
            id=1,
            iban="LE124343567",
            status=status,
            created_at=datetime.utcnow()
        )

        response = await IbanController.validate_iban(
            payload=payload,
            session=None
        )

        assert response.status == status

    @pytest.mark.parametrize(
        "iban,expected",
        [
            ("ME05505000", ValidationStatus.VALID),
            ("LEF5505000012345678951", ValidationStatus.NOT_VALID),
            ("LE05505000000000000000000000000000", ValidationStatus.NOT_VALID),
        ]
    )
    @pytest.mark.asyncio
    async def test_is_valid(self, iban, expected):
        payload = ValidateIbanSchema(iban=iban)
        response = await IbanController.validate_partial_iban(payload=payload)

        assert response.status == expected
