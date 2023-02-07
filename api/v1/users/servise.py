from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User
from ...database import get_session


async def auth_user(token: str = Header(alias="Authorization"), session: AsyncSession = Depends(get_session)) -> User:
    user = await User.find(session, token=token)
    if user:
        return user
    raise HTTPException(401)
