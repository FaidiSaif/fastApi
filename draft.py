posts = [
    {'Post': {'title': '3rd title', 'content': '3rd content', 'published': True, 'id': 4, 'created_at': '2022-07-13T15:53:38.432174+00:00',
              'owner': {'email': 'user2@gmail.com', 'id': 2, 'created_at': '2022-07-13T15:53:38.411465+00:00'}}, 'votes': 0},
    {'Post': {'title': '2nd title', 'content': '2nd content', 'published': True, 'id': 2, 'created_at': '2022-07-13T15:53:38.432174+00:00',
              'owner': {'email': 'user1@gmail.com', 'id': 1, 'created_at': '2022-07-13T15:53:38.166925+00:00'}}, 'votes': 0},
    {'Post': {'title': '3rd title', 'content': '3rd content', 'published': True, 'id': 3, 'created_at': '2022-07-13T15:53:38.432174+00:00',
              'owner': {'email': 'user1@gmail.com', 'id': 1, 'created_at': '2022-07-13T15:53:38.166925+00:00'}}, 'votes': 0},
    {'Post': {'title': 'first title', 'content': 'first content', 'published': True, 'id': 1, 'created_at': '2022-07-13T15:53:38.432174+00:00',
             'owner': {'email': 'user1@gmail.com', 'id': 1, 'created_at': '2022-07-13T15:53:38.166925+00:00'}}, 'votes': 0}
    ]


posts_user_1 = list(filter(lambda p : p['Post']['owner']['id'] == 1 , posts))
print(len(posts_user_1))