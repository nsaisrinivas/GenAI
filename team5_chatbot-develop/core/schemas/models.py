from pydantic import BaseModel
from typing import Optional

class ShowUser(BaseModel):
    id: int
    email: str
    class Config():
        from_attributes=True

class Login(BaseModel):
    username:str
    password:str


class Token(BaseModel):
    access_token: str
    token_type:str

class TokenData(BaseModel):
    email:Optional[str]=None

