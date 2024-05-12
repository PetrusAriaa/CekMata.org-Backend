import datetime
import uuid
import bcrypt
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.applications import JSONResponse
from sqlalchemy.orm import Session

from utils.validate_uuid import validate_uuid
from db import get_db
from models import Users
from dto import UserCreatedResponseModel, CreateUserRequestModel


user_router = APIRouter(tags=["User"])


def __generate_hash(password: str) -> str:
    b_password = password.encode(encoding='utf8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(b_password, salt)
    return str(hashed).split("'")[1]


def __create_user(user_data: CreateUserRequestModel, db: Session) -> str:
    user_id = uuid.uuid4()
    password = __generate_hash(user_data.password)
    user = Users(
        id = user_id,
        created_at = datetime.datetime.now(),
        username = user_data.username,
        password = password
    )
    db.add(user)
    db.commit()
    
    return str(user_id)




# @user_router.get("/")
# def get_users(db: Session = Depends(get_db)) -> JSONResponse:
#     users = db.query(Users).all()
#     return JSONResponse({"username": users[0].username, "password": users[0].password})


@user_router.post("", response_model=UserCreatedResponseModel,
                status_code=status.HTTP_201_CREATED)
def create_user(user_data: CreateUserRequestModel, db: Session=Depends(get_db)):
    user_id = __create_user(user_data, db)
    res = UserCreatedResponseModel(
        code=status.HTTP_201_CREATED,
        data={
            "user_id": user_id,
        }
    )
    return res