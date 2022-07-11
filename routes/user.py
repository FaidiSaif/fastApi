from fastapi import APIRouter, HTTPException,  status, Depends
from sqlalchemy.orm import Session
import schemas
from database import get_db
import models
from typing import List
import utils

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/', response_model=List[schemas.UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{id}', response_model=schemas.UserResponse)
async def get_user(id: int,  db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if (user):
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id  {id} is not Found")
