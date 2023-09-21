from server.core.models import IbanModel
from server.iban.schemas import CreateIbanCheck, UpdateIbanCheck

from .mixins import CreateMixin, UpdateMixin


class IbanDbService(CreateMixin, UpdateMixin):
    table = IbanModel
    create_scheme = CreateIbanCheck  # type: ignore
    update_scheme = UpdateIbanCheck
