from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Annotated, Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from os import getenv
from jose import jwt, JWTError
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    username: str


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


@auth_router.post("/login", response_model=Token)
def local_login(auth_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if auth_data.username != ADMIN_DATA["USERNAME"]:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not exists", headers={'WWW-Authenticate':'Bearer'})

    if auth_data.password != ADMIN_DATA["PASSWORD"]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Wrong username or password", headers={'WWW-Authenticate':'Bearer'})
    
    token_expire = timedelta(minutes=float(getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    token = __generate_token(data={"agent": ADMIN_DATA["USERNAME"]}, expires_delta=token_expire)
    res = JSONResponse({"access_token" : token, "token_type": "bearer", "username": ADMIN_DATA["USERNAME"]})
    return res
