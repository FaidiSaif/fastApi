from fastapi import APIRouter, HTTPException,  status, Depends
from sqlalchemy.orm import Session
import schemas
from database import get_db
import models
from typing import List
import utils
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import database
import oauth2

router = APIRouter(tags=['Authentication'])



# OAuth2PasswordRequestForm
# => means use this route only when OAuth2PasswordRequestForm provided  
# OAuth2PasswordRequestForm => automatically uses 
# {
#   username : "blah", 
#   password : "blah"
# }
# when using OAuth2PasswordRequestForm we need to make the body a form data with key, value and not a raw json body
# it worked for me with params also :p
#

@router.post('/login')
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user: 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    
