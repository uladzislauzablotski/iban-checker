from fastapi import APIRouter

from .iban import router as iban_router

router = APIRouter(prefix="/v1")
router.include_router(iban_router)
