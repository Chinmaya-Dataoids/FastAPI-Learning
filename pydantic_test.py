from pydantic import BaseModel, ValidationError, Field, EmailStr, HttpUrl, SecretStr
from typing import Literal, Annotated
from datetime import datetime, UTC
from uuid import UUID, uuid4

#to create pydantic model , we create a class that inherit from base model
class User(BaseModel):
    #we define fields using type annotations
    #These are required field as they dont have default value
    #annotated is used to add metadata to current type
    #uid: Annotated[int, Field(gt= 0)]
    uid: UUID = Field(alias= "id", default_factory= uuid4)
    username: Annotated[str, Field(min_length= 3, max_length= 20)]
    email: EmailStr
    password: SecretStr
    age: Annotated[int, Field(ge= 13 , le= 130)]

    verified_at: datetime | None = None

    #these are optional fields string as have a default value
    bio: str = ""
    is_active: bool = True

    #if attribute can be multiple things the we also define using '|' for union syntax
    full_name: str | None = None

class BlogPost(BaseModel):

    title: str
    content: str
    view_count: int = 0
    is_published: bool = False

    # lets say we want a list of tags, so that that list we can specify what datatype item should be inside list
    tags: list[str] = Field(default_factory= list)
    # default_factory is just a function that gets called to create a default value each time you create an instance 
    # in theory we can just assign an empty list here like [] but regular classes will share this list with all the instances of a class. So it a bad practise

    #create_at_wrong: datetime = datetime.now(UTC) #this calls datetime.now once when the class is define, so everyblog will have same timestamp
    #create_at_wrong_2: datetime = Field(default_factory= datetime.now(tz= UTC)) #this also wont work as it will alos execute the function when class is defined
    #to default_factory we need to pass an unexecuted function, so basically a function without () 
    create_at: datetime = Field(default_factory= lambda: datetime.now(tz= UTC)) 

    author_id: str | int 

    #literal types - a field/attribute that can only be a specific value , so like enum
    status: Literal["draft","published","archived"] = "draft"


#print(help(BlogPost))

user = User(uid= 123, username = 'Chinmaya', email= 'chinmaya@dataoids.com')

print(user)

#model instance are mutable by default that means they can change
#by default changing field after creation doesnt trigger revalidation which can we changed

user.bio = "Python Developer"
print(user.bio)
print(type(user.bio)) #will output <class int>

#convert model to dict
print(user.model_dump()) #dict
print(user.model_dump_json(indent= 2)) #JSON


try:
    user1 = User(
        uid= "123", # Pydantic has type conversion on by default on we its convert a string in number it wont show that error
        username = None, 
        email= 123
    )
except ValidationError as e:
    print(e)


post = BlogPost(
    title= "Getting Started",
    content = "Here's how...",
    author_id= "12345",
)

print("\n",post)