import uuid
from fastapi import APIRouter, HTTPException, status
from fastapi.applications import JSONResponse
from pydantic import BaseModel

from utils.validate_uuid import validate_uuid


class UserModel(BaseModel):
    username: str
    password: str

user_router = APIRouter(tags=["User"])


def __create_user(user_data: UserModel) -> str:
    user_id = uuid.uuid4()
    print(user_data.username, user_data.password, "halo")
    return str(user_id)


@user_router.get("/")
def create_user(id: str) -> JSONResponse:
    user_id = validate_uuid(id)
    return JSONResponse({'user_id': str(user_id)})


@user_router.post("/")
def create_user(user_data: UserModel) -> JSONResponse:
    user_id = __create_user(user_data)
    return JSONResponse({"status": "success", "user_id": user_id}, status_code=status.HTTP_201_CREATED)