from hashlib import md5

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession

Base = declarative_base()


class Find:
    @classmethod
    async def find(cls, session: AsyncSession, **kwargs):
        kwargs = [getattr(cls, x) == y for x, y in kwargs.items()]
        r = await session.execute(select(cls).where(*kwargs))
        return r.scalar()

    async def create(self, session: AsyncSession):
        session.add(self)
        await session.commit()


class User(Base, Find):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    username: str = Column(String(30), unique=True, nullable=False)
    fullname: str = Column(String(50))
    password: str = Column(String(30), nullable=False)
    token: str = Column(String(32), unique=True, nullable=False)

    sent_mails = relationship("Mail", backref="author", foreign_keys="Mail.author_id", lazy="selectin")
    received_mails = relationship("Mail", backref="recipient", foreign_keys="Mail.recipient_id", lazy="selectin")

    def generate_token(self) -> str:
        return md5(self.password.encode()).hexdigest()

    def __repr__(self):
        return f"User(id={self.id})"


class Mail(Base, Find):
    __tablename__ = "mails"

    id: int = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    content: str = Column(String(1024))
    title: str = Column(String(128))
    read: bool = Column(Boolean, default=False)
    author_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    author: User
    recipient: User

    def __repr__(self):
        return f"Mail(id={self.id})"
