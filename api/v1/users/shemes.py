from pydantic import BaseModel
from pydantic import constr


class AuthUser(BaseModel):
    username: constr(max_length=30)
    password: constr(max_length=30)


class Token(BaseModel):
    token: constr(min_length=32, max_length=32)


class CreateUser(AuthUser):
    fullname: constr(max_length=30)
