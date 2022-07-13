# pip install python-jose[cryptography]
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from requests import Session
from app import database
from app import schemas
from app import models
from fastapi.security import OAuth2PasswordBearer
from app.config import settings

# SECRET_KEY
# Algorithm
# Expiration Time

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})


# get the scheme of the password retrun by the route login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    #data={"user_id": user.id}
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # user_id here must much the payload returned by router.post('/login')
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
        # this exception automatically  return http_401_unauthorized 

    # token data in this case iis TokenData(id) , where id = user_id 
    return token_data

# depends on a token of type oauth2_scheme


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # token in the function args comes from the request
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
