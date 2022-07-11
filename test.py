
from turtle import pos
import psycopg2
from psycopg2.extras import RealDictCursor
import time


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

# insert many products :
posts = [
    {"title": "post1", "content": "content  post1 ",
        "published": False, "owner_id": 9},
    {"title": "post2", "content": "content  post2 ",
        "published": True, "owner_id": 9},
    {"title": "post3", "content": "content  post3 ",
        "published": False, "owner_id": 12},
    {"title": "post4", "content": "content  post4 ",
        "published": False, "owner_id": 14},
    {"title": "post5", "content": "content  post5 ",
        "published": True,  "owner_id": 13},
    {"title": "post6", "content": "content  post6 ",
        "published": False, "owner_id": 13},
    {"title": "post7", "content": "content  post7 ",
        "published": False, "owner_id": 14},
    {"title": "post8", "content": "content  post8 ",
        "published": False, "owner_id": 9},
]


def insert_posts(posts):
    for post in posts:
        cursor.execute(
            """ INSERT INTO posts (title, content , published , owner_id) VALUES (%s,%s,%s, %s) """, (post['title'], post['content'], post['published'], post['owner_id']))
        conn.commit()


if __name__ == "__main__":
    insert_posts(posts)
