from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .shemes import AuthUser, Token, CreateUser
from .servise import auth_user
from ..models import User
from ...database import get_session

router = APIRouter()


@router.post('/', response_model=Token)
async def post(user: CreateUser, session: AsyncSession = Depends(get_session)):
    """
    Create user
    """

    user = User(**user.dict())
    try:
        await user.create(session=session)
    except IntegrityError as exc:
        if exc.orig.args[0] == 1062:
            raise HTTPException(400, "Already exist")
    else:
        return Token(token=user.token)


@router.get('/', response_model=Token)
async def get(user: AuthUser = Depends(), session: AsyncSession = Depends(get_session)):
    """
    Get token of username & password
    """

    user = await User.find(**user.dict(), session=session)
    if user:
        return Token(token=user.token)
    else:
        raise HTTPException(404)
