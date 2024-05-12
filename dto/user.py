from pydantic import BaseModel
from .base_response import BaseResponseModel


class CreateUserRequestModel(BaseModel):
    username: str
    password: str


class UserCreatedModel(BaseModel):
    user_id: str


class UserCreatedResponseModel(BaseResponseModel):
    data: UserCreatedModel