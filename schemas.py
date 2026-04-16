from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, EmailStr
#BaseModel are base class that all of pydantic model ingerit from
#Field - lets us add add contrainsts
#ConfigDict - another modern way to configure model. 

#creating base schema used to cretaing or returning a post
#Without default value means these fields are required

class UserBase(BaseModel):
    username: str = Field(min_length= 1, max_length= 50)
    email: EmailStr = Field(max_length= 120)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes= True)

    id: int
    image_file: str | None
    image_path: str

class UserUpdate(BaseModel):
    
    username: str | None = Field(default= None, min_length= 1, max_length= 50)
    email: EmailStr | None = Field(default= None, max_length= 50)
    image_file: str | None = Field(default= None, min_length= 1, max_length= 200)
    

#--------------------------------

class PostBase(BaseModel):
    title: str = Field(min_length= 1, max_length= 100)
    content: str = Field(min_length= 1)


class PostCreate(PostBase):
    user_id: int

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes= True) #its tell pydantic to read data from object and not just dict , which basically use dot notation as well

    id: int
    user_id: int
    date_posted: datetime
    author: UserResponse

class PostUpdate(BaseModel):

    title: str | None = Field(default= None, min_length= 1, max_length= 100)
    content : str | None = Field(default= None, min_length= 1)
    #user_id is included in update , as its not best practise to allow updation of ownership through partial update endpoint

#------------------------------------


