from fastapi import APIRouter
from .users.router import router as router_users
from .mails.router import router as router_mails

router = APIRouter()

router.include_router(router_users, prefix='/users')
router.include_router(router_mails, prefix='/mails')
