from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from core.models.user import User
from datetime import datetime

class Subscription(SQLModel, table=True):
    __tablename__ = 'subscriptions'

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    name: str = Field(nullable=False)
    concurrent_streams: int = Field(default=1)
    image_quality: str = Field(nullable=False)
    validity_in_days: int = Field(nullable=False)
    price: float = Field(nullable=False)

    user: Optional[User] = Relationship(back_populates="subscriptions")
