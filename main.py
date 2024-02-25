from fastapi import FastAPI
from fastapi.applications import JSONResponse
from fastapi.exceptions import BaseModel
from routes import auth_router, records_router
from dotenv import load_dotenv


load_dotenv(".env.development")

app = FastAPI()

class DummyResponse(BaseModel):
    message: str

@app.get("/", response_model=DummyResponse)
def get_root():
    return JSONResponse({"message": "Hello message"})

app.include_router(prefix="/auth", router=auth_router)
app.include_router(prefix="/records", router=records_router)