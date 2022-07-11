from sqlalchemy import Column, Constraint, Integer, String, Boolean, ForeignKey
from database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

# extend Base model from SQLALchemy

# based on what we defined in the models , if table does not exist sqlAlchemy gonna create it for us
# else it gonna do nothing



# server_default => the default value of the column in the database
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id =  Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable= False)
    # the following line is one of the best feature of sqlAlchemy : you create relationship (it has nothing
    # to do with the constraints) it takes a model name and based on it it figure out the relationship with
    # the current model and then fetch the associated data for it automatically 
    # Post gonna fetch user based on the relationship provided
    # a modification in the scema is also needed to return the fetched user also 
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    #name = Column(String, nullable=False)
