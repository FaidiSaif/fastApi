import pytest
from app import models
from app.oauth2 import create_access_token
from tests.database import session , client

@pytest.fixture()
def test_user_1(client):
    user = {"email": "user1@gmail.com", "password": "user1"}
    res = client.post('/users/', json=user)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user["password"]
    return new_user


@pytest.fixture()
def test_user_2(client):
    user = {"email": "user2@gmail.com", "password": "user2"}
    res = client.post('/users/', json=user)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user["password"]
    return new_user


# authentictae test_user_1
@pytest.fixture()
def token(test_user_1):
    return create_access_token({"user_id": test_user_1['id']})

# authorize the client with token(of tets_user_1)
@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
       "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture()
def test_posts(session, test_user_1, test_user_2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user_1['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user_1['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user_1['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user_2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)
    posts = list(map(create_post_model, posts_data))
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
