from fastapi.testclient import TestClient
from app.database import get_db, Base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy import create_engine
from app.main import app
import pytest


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

# engine is what is responsible to connect to the db from the ORM
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# drop the previous tables and create new tables for testing
# this fixture cleans the db , creates the required tables and return a db session and return it


@pytest.fixture()
def session():
    print("session fixture run...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):  # since there is a session passed as parameter then the current fixture gonna run the session fixture before the current
    # Dependency => this will be passed to the decorator of the endpoint so it's gonna be called every time a call to the endpoint is made
    # so after a get request for example the db.close gonna be called thanks to the deco (no need to manually call it every time)
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    # tells pytest to use override_get_db (the db session pointing tp fast_ap_test and not fastapi)
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

