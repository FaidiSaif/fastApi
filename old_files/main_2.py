# this exmaple uses a db with no ORM

from email import message
from os import stat
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# RealDictCursor => allows the display of a mapping between the returned values of a query and the column names


def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(dbname='fastapi', port=49155,
                                    password='postgres', user='postgres', cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print('Database connection was successful')
            return conn, cursor
        except Exception as error:
            print("Connecting to databse failed")
            print('Error: ', error)
            time.sleep(2)


conn, cursor = connect_to_db()
# print(cursor)


# this inheritance defines a data model so that the request body should be resppected
# i.e. this is a way to enforce the data types and the json keys
class Post(BaseModel):  # " this is a pydantic model"
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None


@app.get('/posts')
async def get_posts() -> dict:
    cursor.execute(" SELECT * FROM posts")
    my_posts = cursor.fetchall()
    print(my_posts)
    return {
        "data": my_posts
    }


@app.get('/posts/{id}')
# type here tells fastApi to convert id as integer not string anymore
async def get_post(id: int):
    # there is no need to convert id to integer here
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    m_post = cursor.fetchone()
    if (m_post):
        return {"data":  m_post}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id  {id} is not Found")


# when delete succeed , then the status code is 204 ! (kinda weird)
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:  int) -> dict:
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    post = cursor.fetchone()
    if (post):
        cursor.execute(
            """ DELETE FROM posts WHERE id = %s RETURNING* """, (id,))
        print('deleted post :  ', cursor.fetchone())
        conn.commit()
        # if you return a data you gona get the following error : RuntimeError: Response content longer than Content-Length
        # return {'deleted_post': item, 'message': 'your post is deleted'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id  {id} is not Found")


# fastApi validates the data for us thanks to pydantic and the Post type :)
@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_post(post: Post) -> dict:
    cursor.execute(
        """ INSERT INTO posts (title, content , published ) VALUES (%s,%s,%s) RETURNING* """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {
        "data": new_post  # dict here comes from the pydantic model
    }


@app.put('/posts/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_post(id: int, post: Post) -> dict:
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    item = cursor.fetchone()
    if (item):
        cursor.execute(
            """ UPDATE posts SET title=%s,  content=%s , published=%s WHERE id=%s RETURNING* """, (post.title, post.content, post.published, id))
        res = cursor.fetchone()
        conn.commit()
        return {
            "data": res  # dict here comes from the pydantic model
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id  {id} is not Found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
