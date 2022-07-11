from datetime import datetime
from secrets import token_bytes
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

# this inheritance defines a data model so that the request body should be resppected
# i.e. this is a way to enforce the data types and the json keys






#user schemas 
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int 
    created_at: datetime

    class Config:
        orm_mode = True



# post schema
class PostBase(BaseModel):  # " this is a pydantic model"
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

class PostCreate(PostBase):
    pass

# defining the return schema using a new Model
class Post(PostBase):
    id: int
    created_at: datetime
    owner : UserResponse

    class Config:
        orm_mode = True

# after adding the votes to the return value the result is transformed to {Post : 'balabla' , votes : int} => that's why we added this schema 
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True



#auth schemas 
class UserLogin(BaseModel): 
    email : EmailStr
    password : str 

class Token (BaseModel) :
    access_token : str 
    token_type : str 



class TokenData(BaseModel): 
    id : Optional[str]



## schema for vote 
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
