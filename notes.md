# https://github.com/Sanjeev-Thiyagarajan/fastapi-course

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


# alembic (the git of the database )
is the tool responsible for migrating database 
- first step is to init alembic : alembic --init 
- need to have access to the declarative Base object in the alembic/env.py
- in the alembic env.py override the sqlalchemy.url variable coming from the almebic.ini file using config.set_main_option
- important to import Base from the models file (to alow alembic to read all the tables) and not from database
- when creation a revision with alembic , it generates a file for you where you have to  implement the
upgradinging and downgrading logics 
- to create a revision  : alembic revision -m "message to tag this revision"
- to run a revision function : alembic upgrade ccdrf5r5 (from the revision file)
- to go to the previous rev : alembic downgrade -1 
- to go to the next rev : alembic downgrade +1 , up 2  rev : alembic downgrade +2
- upgrade to the last rev : alembic upgrade head   
- if you want to auto-generate a revision from the existing models 
you can use alembic revision --autogenerate -m "ypur-message"
=> alembic did this automatically thanks to the target_metadata we set in the env.py 

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

# jointure 
SELECT *
FROM A
INNER JOIN B ON A.key = B.key

# convention forign keys
assume table posts has owner_id which reference the user is in the users table 
so source : posts & target : users 
convention naming : source_target_fk => posts_users_fk 

# alembic in prod
-don't create revision in the prod env 
-just check the revision created in the dev env 

# --host 
-by default when your run a server in the machine it listen on the 127.0.0.1 ip address 
-if your machine has many ip @ like 127.0.0.1 and 192.168.0.44 and you want your server to nbe listinig on all the @
=> provide the --host 0.0.0.0 option , now it listens to all the addresses 
## uvicorn --host 0.0.0.0 app.main:app

# gunicorn 
- pip install gunicorn 
- pip install httptools 
- pip install uvloop

gunicorn --workers => set up  the number of workers 

# nginx
nginx is a more professional way to loadbalance the requests 
using guincorn is fine but it does not handle proxy, ssl ...
nginx is an intermediate web server high peroformant and optimised for SSL termination (https requets)
-if we use our app to handle ssl we gonna see degradation in performance that's why we use nginx 
==== https ====> nginx ====> http ====> guincorn , it forward https requests to the app in the form of http

# firewall 
if you want to access your db remotly : enable port 5432(for the db) to be remotly accessbile 

# docker 
docker does not run all the steps each time , it caches the steps in dockerfile and only runs the the remaining 
steps, see 13:30

# bind mount 
it syncs folder from machine and folder in docker image 
so don't need to remove the image every time and recreate it 
in your docker-compose service we added a volumes section where you specify the associated path 
/./:/usr/src/app:ro => ro stands for read only , paths to be in syncs from docker image and localhost 
- normally we don't need command section in docker compose because we have it in dockerfile
but because even when making changes are updates thanks to bind mount the docker compose 
file is not reloading 


# testing 
running a test  => py -3 tests\test_calculations.py
by default pytest looks for all the files matching the pattern  *_test.py , test_*.py
so when you run hte command "pytest" => it looks for all the matching files and runs the associated tests
=> this is called auto-discovery
methods should match the pattern test_*
by default pytest does not ruin you print statement , to make it do so add the -s flag 
-x option : stop after the first fail 
# fixture
is a function that runs before each test  

#  /users/ or /users
- when using only /users => pytest gonna automatically redirects you to /users/
- /users causes an issue because the http return code is 307 , becuase of the redirection => make sure you use /users/


# in pytest form-data
- when you send data as form data for login use the arg data=
- when you send data as body use the arg json= 


# fixture scopes
- id fixture going to run once by function , class , module...(by default it's set to function)
- pytest run the tests in the order from top to bottom   

# conftest 
this file has all the fixtures 

# run test
1- specific file : pytest -v -s .\tests\test_posts.py
2- all pytest -v -s s