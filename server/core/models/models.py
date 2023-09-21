from datetime import datetime

from sqlalchemy import BigInteger, Column, DateTime, Enum, String

from server.core.enums import ValidationStatus
from server.core.models.base_model import BaseModel


class IbanModel(BaseModel):
    __tablename__ = 'iban'

    id = Column(BigInteger, primary_key=True, index=True)
    iban = Column(String)
    status = Column(Enum(ValidationStatus))

    created_at = Column(DateTime, default=datetime.utcnow())
