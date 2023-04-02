from fastapi import FastAPI, HTTPException, status, Response, Depends
from fastapi.params import Body
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

# command that creates database schemas in postgres
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost',
                         database='socialmedia_api',
                         user='postgres',
                         password='pAlcacer9!',
                         cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print('Database connection was succesfful!!')
        break

    except Exception as e:
        print(f'Error: {e}')
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "Hello World!!!"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()

    posts = db.query(models.Post).all()

    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (new_post.title, new_post.content, new_post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title,
    #                        content=post.content,
    #                        published=post.published)

    new_post = models.Post(**post.dict())           # ** unpacks dictionary

    db.add(new_post)
    db.commit()
    db.refresh(new_post)        # retrieve the stored post
    return {'data': new_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()         # stop looking in db once object is found
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} not found.')
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)       # only returns query

    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with ID {id} does not exist.')

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute(""" UPDATE posts SET title= %s, content= %s WHERE id= %s RETURNING *""",
    #                (post.title, post.content, str(id)))
    #
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with ID {id} does not exist.')

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {'updated post': post_query.first()}




