from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from core.models.user import User
from core.models.subscription import Subscription
from datetime import datetime

class SubscriptionPlan(SQLModel, table=True):
    __tablename__ = 'subscription_plans'

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='users.id')
    subscription_id: int = Field(foreign_key='subscriptions.id')
    start_date: datetime = Field(nullable=True)
    end_date: datetime = Field(nullable=True)

    user: Optional['User'] = Relationship(back_populates='subscription_plans')
    subscription: Optional['Subscription'] = Relationship(back_populates='subscription_plans')
