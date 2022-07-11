launch the app: 
  uvicorn main:app --reload


# Read from url with FastApi
async def get_post(id: int , response : Response):
  pass
 
type here tells fastApi to convert id as integer not string anymore,
because by default the id arsed from the url is considered as string 


# override the resposne by setting the response variable 
the response can be passed as a callback to the endpoint function 
taht response is automatically send to the client  

async def get_post(id: int , response : Response):
  if (error) :
    response.status_code = 404
instead of doing the above we can raise HTTPException => a lot cleaner 


# update the post list : 
 -find the index in the list and then affect to it the new post , my_posts[index] = new_post 
 -find the post itself and then update it with the correct value 
 => i think the first one is easier 

# documentation 
the docs is generated automatically 
got to : /domain/docs for swagger 
got to : /domain/redoc for rdoc docs 
=> use the one you prefer 

# to use a folder as a package 
-add __init__.py  to the folder ( you want it to become your package)
-beause we moved the main file to the app package => need to update the uvicorn command from uvicorn main:app --relaod to uvicorn app.main:app --reload 


# RealDictCursor
RealDictCursor => allows the display of a mapping between the returned values of a query and the column names


# when using RETURNING* ; at the end a sql query 
=> this allows getting the result of the query using the fetchone function 
example : 
cursor.execute(""" INSERT INTO posts (title, content , published ) VALUES (post.title, post.content, post.published) RETURNING* """)
inserted_post =  cursor.fetchOne()

# don't use string formatting in sql query 
=> the code can be vulnerable to sql injection 

# psycopg2 
this is the driver for postgres database
-if you are using mysql for example => find the associated driver 

# sqlAlchemy
it's an ORM allowing to  translate regular python code into sql query  
-> it gonna need the driver (psycopg2 in our case )


# models 
every model represents a table in our database

# get_db ?
#Dependency => this will be passed to the decorator of the endpoint so it's gonna be called every time a call to the endpoint is made 
so after a get request for example the db.close gonna be called thanks to the deco (no need to manually call it every time)
def get_db(): 
    db = SessionLocal()
    try :
        yield db 
    finally :
        db.close()


# alembic
is the tool responsible for migrating database 

# pydantic model vs sqlAlchemy model
- pydantic :  defines the shape of the request, the request model 
- sqlAlchemy : defines the db model , how the db gonna look like 
=> in general pydantic_model + sql_alchemy_default_values = sql_alchemy_model 
- it's possible to devide the the request and resposne into 2 different models 

# passwd in db 
never store password as a string always hash it 
-use passlib to handle the hash 
-use bcrypt to define the hash algo
=> make sure both libraries are installed 


# APIRouter 
- create a routers folder where you create the scripts for different routes (user & post for example)
- instatiate a router object router = APIRouter() and then use it to define the routes 
 router.post('/posts')
 def create_post(..):
  pass

- include all the  all the routes in the main script using : app.include_router(post.router) and app.include_router(user.router) 

int the APiRouter instance you can define 
- tags   => useful for documentation in openApi to seperate each section 
- prefix => allows to avoid repeating the same subpath in every route  

# what is the signature in jWT
it's the result of combining header + payload + secret 
where the secret is only stored in the api , it can not exist in the front end 
=> after creating the signature we generate a JWT token with w hash function .
every time we make a request our api gonna regenerate a test signature and compare it to the one coming from the jwt token.

=> using this logic hackers can not generate tokens for other users because it's based on the signature which is only in the backend 


# hasing is only one way
- once passwd is hashed it can not be retrieved again 
- to compare it to a test_passwd you need to hash the test_passwd and see if they are equal 
according to the example if 2 passwords are equal they have the same hash (based on the same algo) 
!! not what i have seen :/ 


# verify token 
-pip install python-jose[cryptography] 

# postman envirement variables
in postman it's possible to create env vars to avoid changing vars in every request