from typing import List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = 'users'

    id: int = Field(default=None, primary_key=True)
    email: str = Field(nullable=False, index=True)
    password: str = Field(nullable=False)
    session_token: str = Field(nullable=True)
    session_expiry_time: datetime = Field(nullable=True)

    subscriptions: List['Subscription'] = Relationship(back_populates='user')
    