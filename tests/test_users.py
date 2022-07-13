from http import client
from msilib import schema
from fastapi.testclient import TestClient
import pytest

# fix this later => adding __init__ file to this package add the path to the sys path so noj need to do the following lines
# import sys
# sys.path.append("C:\\Users\\saif\\Desktop\\tutos\\python\\fastApi")

from app import schemas
from app.oauth2 import verify_access_token, credentials_exception


# def test_root(client):
#   res = client.get('/')
#   assert res.json().get('message') == 'hello world'
#   assert res.status_code == 200
#   print(res.json())


def test_create_user(client):
    res = client.post(
        '/users/', json={"email": "hello123@gmail.com", "password": "12345"})
    # using pydantic here allows doing some validation for us , no need to check the schema of the resposne manually
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


# test a user test_user login the extracted id from it's token is the same as it's id
def test_login_user(client, test_user_1):
    res = client.post(
        '/login', data={"username": test_user_1['email'], "password": test_user_1['password']})

    login_res = schemas.Token(**res.json())
    token_data = verify_access_token(
        login_res.access_token, credentials_exception)
    assert token_data.id == str(test_user_1['id'])
    assert res.status_code == 200
    assert login_res.token_type == "bearer"


@pytest.mark.parametrize("email, password, status_code", [
 ('incorrect_mail', 'test', 403),
 ('work_mail', 'wrong_password', 403),
 ('test@gmail.com', 'incorrect_password', 403),
 (None, 'passwd', 422),
 ("test@gmail.com", None, 422)
 ])
def test_incorrect_login(client, email, password, status_code):
    res = client.post(
        '/login', data={"username": email, "password": password})
    assert res.status_code == status_code
