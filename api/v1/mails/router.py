from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .shemes import CreateMail, GetMails
from .servise import get_mails, read_mail
from ..models import User, Mail
from ...database import get_session
from ..users.servise import auth_user

router = APIRouter()


@router.post('/')
async def post(mail: CreateMail, user: User = Depends(auth_user), session: AsyncSession = Depends(get_session)):
    """
    Create mail
    """

    mail = Mail(**mail.dict(), author_id=user.id)
    await mail.create(session=session)


@router.get('/', response_model=GetMails)
async def get(user: User = Depends(auth_user), session: AsyncSession = Depends(get_session)):
    """
    Get mails
    """

    r = await get_mails(user=user, session=session)
    return {'mails': r}


@router.post('/read/{mail_id:int}')
async def post(mail_id: int, user: User = Depends(auth_user), session: AsyncSession = Depends(get_session)):
    """
    Read mail
    """
    mail = await Mail.find(id=mail_id, recipient_id=user.id, session=session)
    if not mail:
        raise HTTPException(404)
    await read_mail(mail=mail, session=session)
