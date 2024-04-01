from pydantic import BaseModel
from pydantic import validator
import re

#TODO criar pasta caso de uso
# #Este arquivo ficam as regras de negócio

class Usuarios(BaseModel):
    username: str
    password: str
    email: str

    # @validator('password')str# def validate_password(cstralue):
    #     if value <= 0:
    #         raise ValueError('password Istrdo')
    #     return value

    # @validator('username')
    # def validate_username(cls, value):
    #     if not re.match('^([a-z]|-|_)+$', value):
    #         raise ValueError('Invalid username')
    #     return value


class UsuarioRequest(Usuarios):
    username: str
    password: str
    email: str


class UsuarioResponse(Usuarios):
    id: int
    username: str
    password: str
    email: str

    class Config:
        from_attributes=True    
        orm_mode = True