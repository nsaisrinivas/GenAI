from fastapi import Depends, FastAPI, HTTPException, Header, Form,status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Optional, Annotated,List

from core.models import database
from core.crud import user as user_crud
from core.crud import subscription as subscription_crud
from core.models.user import User
from sqlmodel import Session

from core.schemas.models import ShowUser,Login
from core.hashing.bcrpt import Bcrpyt
from core.jwt.tokens import get_current_user
from datetime import datetime,timedelta

from core.jwt.tokens import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
database.create_db_and_tables()
app = FastAPI()

def get_db():
    db = Session(database.engine)
    try:
        yield db
    finally:
        db.close()

#Login
@app.post("/login" , tags=["login"])
async def Login(request:OAuth2PasswordRequestForm = Depends(), db_session:Session=Depends(get_db)):
     with db_session:
          user= user_crud.findByUsername(request,session=db_session)
          if not user:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
          if not (Bcrpyt.verify_password(request.password,user.password)):
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect Password")
          # access_token_expires= timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
          access_token = create_access_token(data={"sub": user.email})
          return {"access_token": access_token, "token_type": "bearer"}
     
#display list of all users        
@app.get('/users' , response_model=List[ShowUser] ,tags=["users"])
async def users(db_session: Session = Depends(get_db)):
    with db_session:
        users = user_crud.get_users(session=db_session)
    return users

#Create a new User
@app.post('/users/save' ,response_model=ShowUser, tags=["users"], status_code=status.HTTP_201_CREATED)
async def saveUser(user: User , db_session: Session=Depends(get_db)):
     with db_session:
          user.password= Bcrpyt.Pass_enc(user.password)
          newUser = user_crud.saveUser(user,session=db_session)
     return newUser

#Get the user by Id
@app.get("/user/{id}" ,response_model=ShowUser, tags=["users"])
async def findUser(id: int, db_session:Session=Depends(get_db), get_current_user:Login=Depends(get_current_user)):
     with db_session:
          user=user_crud.findUser(id,session=db_session)
     if user:
          return user
     else:
          raise HTTPException(detail=f"user with id: {id} not found", status_code=status.HTTP_404_NOT_FOUND)
     
#Delete the user by Id
@app.delete("/user/{id}" ,tags=["users"], status_code=status.HTTP_204_NO_CONTENT)
async def deleteUser(id:int , db_session:Session=Depends(get_db)):
     with db_session:
        user=user_crud.deleteUser(id,session=db_session)
        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id:{id} not found")

#Update the existing user by id
@app.put("/user/{id}" , tags=["users"])
async def updateUser(id:int, user:User, db_session:Session=Depends(get_db)):
     with db_session:
          user=user_crud.updateUser(id,user,session=db_session)
          if user:
               return user
          else:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id:{id} not found")

#Get the list of all subscriptions
@app.get('/subscriptions' ,tags=["subscription"])
async def subscriptions(db_session: Session = Depends(get_db)):
    with db_session:
        subscriptions = subscription_crud.get_subscriptions(session=db_session)
    return subscriptions

@app.post('/chat')
async def respond_to_chat(query: Annotated[str, Form()],
                            session_token: Optional[str] = Header(None),
                            db_session: Session = Depends(get_db)):
            request_time = datetime.now()
            formatted_time = request_time.strftime("%Y-%m-%d %H:%M:%S")
            return { 'query': query, 'response': f"Echoing {query}", 'request_time': formatted_time}
