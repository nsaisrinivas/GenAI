from sqlmodel import Session, select
from core.models.subscription import Subscription

def get_subscriptions(session: Session):
    statement = select(Subscription)
    subscriptions = session.exec(statement).all()
    return subscriptions
