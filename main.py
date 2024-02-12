from fastapi import FastAPI
from fastapi.applications import JSONResponse
from fastapi.exceptions import BaseModel

app = FastAPI()

class DummyResponse(BaseModel):
    message: str

@app.get("/", response_model=DummyResponse)
def get_root():
    return JSONResponse({"message": "Hello message"})