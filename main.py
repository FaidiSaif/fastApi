# this exmaple uses a db with no ORM
from fastapi import FastAPI
from database import   engine
import models
from routes import post , user , auth , vote 
from fastapi.middleware.cors import CORSMiddleware

# this is the first line to run when the code is triggered => gonna create our tables (if they don't exist)
# no need to use this command anymore with alembic 
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
