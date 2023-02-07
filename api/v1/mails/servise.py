from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User, Mail


async def get_mails(user: User, session: AsyncSession):
    q = select(Mail).where((Mail.author_id == user.id) | (Mail.recipient_id == user.id))
    results = await session.execute(q)
    return [x[0] for x in results.all()]


async def read_mail(mail: Mail, session: AsyncSession):
    mail.read = 1
    await session.commit()
