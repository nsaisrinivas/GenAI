from sqlmodel import Session, select, update
from core.models.user import User
from core.schemas.models import Login

def get_users(session: Session):
    statement = select(User)
    users = session.exec(statement).all()
    return users

def saveUser(user:User , session: Session):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def findUser(id:int , session:Session):
    user=session.query(User).filter(User.id==id).first()
    return user

def deleteUser(id:int , session=Session):
    user=session.query(User).filter(User.id==id).first()
    # print(user)
    if user:
        session.delete(user)
        session.commit()
        return user
    else:
        return None
    
def updateUser(id:int, user:User , session=Session):
    user=session.query(User).filter(User.id==id)
    print(user)
    if user.first():
        session._update_impl(user)
        session.commit()
        session.refresh()
        return user
    else:
        return None

def findByUsername(user:Login, session=Session):
    found_user=session.query(User).filter(User.email==user.username).first()
    if(found_user):
        return found_user
    else:
        return None