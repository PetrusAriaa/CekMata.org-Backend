import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from os import getenv
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from db import get_db
from dto import TokenResponseModel
from models import Users


ADMIN_DATA = {
    "USERNAME": "admin",
    "PASSWORD": "admin"
}

oauth2_token_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

auth_router = APIRouter(tags=["Authentication"])


def __generate_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, getenv("SECRET"), getenv("ALGORITHM"))
    return token


def __validate_password(password: str, true_password:str) -> bool:
    b_password = password.encode(encoding='utf-8')
    return bcrypt.checkpw(b_password, bytes(true_password, encoding='utf-8'))


def validate_token(token: Annotated[str, Depends(oauth2_token_scheme)]):
    credential_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate token",
        headers={'WWW-Authenticate': 'Bearer'}
        )
    try:
        payload = jwt.decode(token, getenv("SECRET"), getenv("ALGORITHM"))
        return payload
    except JWTError:
        raise credential_error


@auth_router.post("/login", response_model=TokenResponseModel, status_code=status.HTTP_200_OK)
def local_login(auth_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session=Depends(get_db))  -> TokenResponseModel:
    user = db.query(Users).filter(Users.username==auth_data.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found",
                            headers={'WWW-Authenticate': 'Bearer'})

    if not __validate_password(auth_data.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Wrong username or password", headers={'WWW-Authenticate':'Bearer'})
    
    token_expire = timedelta(minutes=float(getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    token = __generate_token(data={"agent": ADMIN_DATA["USERNAME"]}, expires_delta=token_expire)
    res = TokenResponseModel(
            access_token = token,
            token_type = "Bearer",
            username = user.username
            )
    return res
