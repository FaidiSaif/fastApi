from venv import create
from sqlalchemy import create_engine, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings 
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
#SQLALCHEMY_DATABASE_URL  = 'postgresql://postgres:postgres@localhost:49155/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine is what is responsible to connect to the db from the ORM
engine = create_engine(SQLALCHEMY_DATABASE_URL )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


#Dependency => this will be passed to the decorator of the endpoint so it's gonna be called every time a call to the endpoint is made 
# so after a get request for example the db.close gonna be called thanks to the deco (no need to manually call it every time)
def get_db(): 
    db = SessionLocal()
    try :
        yield db 
    finally :
        db.close()