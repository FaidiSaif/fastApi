from fastapi import APIRouter,  status, HTTPException, Depends
from sqlalchemy.orm import Session
import schemas
from database import get_db
import models
from typing import List
import oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get('/', response_model=List[schemas.Post])
async def get_posts(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts


@router.get('/{id}', response_model=schemas.Post)
async def get_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id ==
                                        id).first()  # better than all in this case

    if (post):
        return post
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id  {id} is not Found")


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:  int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    if (post):
        post_query.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id  {id} is not Found")


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)) -> dict:
    # Inserting data into the database is a three step process:
    #    Create the Python object
    #    Add it to the session
    #    Commit the session
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    # this is equivalent to the RETURNING* in the sql query
    db.refresh(new_post)
    return new_post


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)) -> dict:

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_to_update = post_query.first()

    if post_to_update == None : 
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id  {id} is not Found")
    if post_to_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    # db.refresh(post_to_update) it possible to use the refresh but in this example i'm gonna use the first method on the query object
    return post_query.first()
    
