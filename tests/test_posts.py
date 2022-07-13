from venv import create
import pytest
from app import schemas
from tests.conftest import test_user_1


def test_all_posts(test_user_1, authorized_client, test_posts):
    # the create_posts creates 4 posts where 3 created by test_user_1 and 1 created by test_user_2
    res_posts = authorized_client.get('/posts')
    posts = res_posts.json()
    posts_user_1 = list(filter(lambda p: p['Post']['owner']['id'] == 1, posts))
    # valide schema of the results
    validated_posts = list(
        map(lambda post: schemas.PostOut(**post), posts))
    # assertions
    assert len(list(posts_user_1)) == 3
    assert len(posts) == 4
    assert res_posts.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts')
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    # test_posts[0]["id"] does not work because the test_posts[0] is an objectb and not a dictionary
    res = client.get(f'/posts/{test_posts[0].id}')
    #print('------' *50, test_posts[0])
    assert res.status_code == 401


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    # validate the schemas
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200


@pytest.mark.parametrize('title, content, published', [
    ('t11', 'c11', True),
    ('t22', 'c22', False),
    ('t33', 'c33', True)
])
def test_create_posts(authorized_client, test_user_1, title, content, published):
    res = authorized_client.post('/posts/', json={
        "title": title,
        "content": content,
        "published":  published,
    })
    created_post = schemas.Post(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert res.status_code == 201


def test_unauthorized_user_create_post(client):
    res = client.post('/posts/', json={
        "title": "any title",
        "content": "any content",
        "published":  False,
    })
    assert res.status_code == 401 #Unauthorized 



def test_delete_post_success(authorized_client,  test_posts): 
  # i'm sure that post number 1 is created by test_user_1
  res = authorized_client.delete(f'/posts/{test_posts[0].id}')
  assert res.status_code == 204


def test_delete_post_unauthorized(client,  test_posts): 
  # i'm sure that post number 1 is created by test_user_1
  res = client.delete(f'/posts/{test_posts[1].id}')
  assert res.status_code == 401


def test_delete_other_user_post(authorized_client, test_posts): 
  #post 2 is the post associated to test_user_2 but authorized_client is associated to test_user_1
  res = authorized_client.delete(f'/posts/{test_posts[3].id}')
  assert res.status_code == 403 #forbidden 



def test_update_other_user_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404