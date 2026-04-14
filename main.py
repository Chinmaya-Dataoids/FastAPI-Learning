#basic fastapi app
from typing import Annotated

from fastapi import FastAPI,Request, HTTPException, status, Depends
from fastapi.exceptions import RequestValidationError # for handling validation errors like data type mismatched
from fastapi.responses import JSONResponse 
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
#fastapi is buld on top starlette so to catch starlette error we uses its HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException 

from schemas import PostCreate , PostResponse, UserCreate, UserResponse
from sqlalchemy import select #for querying
from sqlalchemy.orm import Session

import models
from database import Base, engine, get_db

#create table
Base.metadata.create_all(bind= engine)

#intialised app object
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount("/media", StaticFiles(directory='media'), name= "media")

templates = Jinja2Templates(directory="templates")


#use decorators for routes

#########------------------Normal Web pages routes--------------------#########################

@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "home.html",
        {"posts": posts, "title": "Home"},
    )

@app.get("/posts/{post_id}", include_in_schema=False)
def post_page(request: Request, post_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        title = post.title[:50]
        return templates.TemplateResponse(
            request,
            "post.html",
            {"post": post, "title": title},
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.get("/users/{user_id}/posts", include_in_schema=False, name="user_posts")
def user_posts_page(
    request: Request,
    user_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = result.scalars().all()
    return templates.TemplateResponse(
        request,
        "user_posts.html",
        {"posts": posts, "user": user, "title": f"{user.username}'s Posts"},
    )

#########------------------API routes--------------------#########################
@app.post(
    "/api/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
#annotated is used here for dependecy injection, so before running this function run get_db function and pass the response to db parameter
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    
    result = db.execute(
        select(models.User).where(models.User.username == user.username)
    )
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Username already exists"
        )
    
    result = db.execute(
        select(models.User).where(models.User.email == user.email)
    )
    existing_email = result.scalars().first()

    if existing_email:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "Email already exists"
        )
    
    new_user = models.User(
        username= user.username,
        email= user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/api/users/{user_id}", response_model= UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.User).where(models.User.id == user_id)
    )

    
    user = result.scalars().first()

    if user:
        return user
    
    raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail = "User NOT found"
    )

@app.get("/api/users/{user_id}/posts", response_model=list[PostResponse])
def get_user_posts(user_id: int, db: Annotated[Session, Depends(get_db)]):

    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    result = db.execute(select(models.Post).where(models.Post.user_id == user_id))
    posts = result.scalars().all()
    return posts

#Using response_model fastapi will validate tha each post matches our post response schema
@app.get("/api/posts", response_model=list[PostResponse])
def get_posts(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts

## Create Post
@app.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == post.user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    new_post = models.Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@app.get("/api/hosts")
def get_hosts():
    return {"message": 'Hi'}

#these are path parameters and not query parameters
@app.get("/api/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().first()
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")



#########------------------Exceptions--------------------#########################

## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    #if startlette doesnt return a detail
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )
    #now if its api route then JSON response else HTTP template response
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )




### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )