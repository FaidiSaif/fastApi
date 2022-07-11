## this example uses a list of data not a db 

from email import message
from os import stat
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException

from pydantic import BaseModel
from random import randrange

from test import connect_to_db

app = FastAPI()

my_posts = [
    {"title": "post_1", "content": 'content for post 1', "id": 1}, {
        "title": "post_2", "content": 'content for post 2', "id": 2}]
# this inheritance defines a data model so that the request body should be resppected
# i.e. this is a way to enforce the data types and the json keys

cursor = connect_to_db()
#print(cursor)

class Post(BaseModel):  # " this is a pydantic model"
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get('/posts')
async def get_posts() -> dict:
    return {
        "data": my_posts
    }


@app.get('/posts/{id}')
# type here tells fastApi to convert id as integer not string anymore
async def get_post(id: int):
    # there is no need to convert id to integer here
    m_post = next(filter(lambda p: p.get('id') == id, my_posts), None)
    if (m_post):
        return {"data":  m_post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id  {id} is not Found")


# when delete succeed , then the status code is 204 ! (kinda weird)
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:  int) -> dict:
    item = next(filter(lambda post: post.get('id') == id, my_posts), None)
    if (item):
        my_posts.remove(item)
        #if you return a data you gona get the following error : RuntimeError: Response content longer than Content-Length
        #return {'deleted_post': item, 'message': 'your post is deleted'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id  {id} is not Found")


# fastApi validates the data for us thanks to pydantic and the Post type :)
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post) -> dict:
    new_post = post.dict()
    new_post['id'] = randrange(3, 100000)
    my_posts.append(new_post)
    return {
        "data": new_post  # dict here comes from the pydantic model
    }


@app.put('/posts/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_post(id: int, post: Post) -> dict:
    fetched_post = next(filter(lambda post: post.get('id') == id, my_posts), None)
    if (fetched_post):
        fetched_post.update({**fetched_post,**post.dict()}) 
        return {
            "data": fetched_post  # dict here comes from the pydantic model
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id  {id} is not Found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)