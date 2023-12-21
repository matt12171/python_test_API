from typing import Optional, List
from sensitive import mongo_connection_string
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument


app = FastAPI()

# Link to mongoDB 
# mongo_connection_string is saved in another file and imported here so that it is not added to github as it conatins db password
client = motor.motor_asyncio.AsyncIOMotorClient(mongo_connection_string)

# This names the DB. Change it to anything that suits - Here it is called test
db = client.test

# Sets up a mongoDB collection called users
user_collection = db.get_collection("users")

# Changes ID to a string - mongoDB automatically creates an ID for anything inserted into it.
PyObjectId = Annotated[str, BeforeValidator(str)]


class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str = Field(...)
    location: str = Field(...)
    skills: str = Field(...)
    interests: str = Field(...)


class UserCollection(BaseModel):
    """
    A container holding a list of `StudentModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    users: List[UserModel]












# Very basic post request - more options can be added to this to define what we want the post body to look like
@app.post('/user',response_description="Add new student",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,)

# async is the same as using promises in JS
# This function gets executed when a post request is made
async def create_user(user: UserModel = Body(...)):
    # Inserting the new user into mongoDB 
    new_user = await user_collection.insert_one(
        # model_dump is a pydantic thing which converts a model to a dictionary 
        user.model_dump(by_alias=True, exclude=['id'])
    )
    # Grabbing the newly inserted user using user_collection.find_one()
    created_user = await user_collection.find_one(
        {'_id': new_user.inserted_id}
    )

    # Had to change id into a string
    # created_user['_id'] = str(created_user['_id'])
    # Returning the newly inserted user - this is the response to the post request
    return created_user

# Simple get request for all users
@app.get('/users', response_model=UserCollection,
    response_model_by_alias=False,)

# function runs once a get request is sent
async def list_users():
    # grabs all users from collection using find().to_list(1000)
    return UserCollection(users=await user_collection.find().to_list(1000))