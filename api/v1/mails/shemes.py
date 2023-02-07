from typing import List, Union
from pydantic import BaseModel
from pydantic import constr


class Mail(BaseModel):
    id: int
    content: constr(max_length=1024)
    read: int
    author_id: int
    recipient_id: int

    class Config:
        orm_mode = True


class CreateMail(BaseModel):
    recipient_id: int
    content: constr(max_length=1024)
    title: constr(max_length=128)


class GetMails(BaseModel):
    mails: List[Mail]

    class Config:
        orm_mode = True
