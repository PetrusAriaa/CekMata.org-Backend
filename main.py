from fastapi import FastAPI, status
from fastapi.applications import JSONResponse
from dto.base_response import HealthCheckModel
from routes import auth_router, records_router, user_router, predictor_router
from dto import HealthCheckResponseModel
# from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


# load_dotenv(".env.development")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_credentials=True,
    allow_headers=['*']
)


@app.get("/health", response_model=HealthCheckResponseModel, tags=['HealthCheck'])
def health_check() -> HealthCheckResponseModel:
    res = HealthCheckResponseModel(
        code=status.HTTP_200_OK,
        data=HealthCheckModel(
            status="up and running",
        )
    )
    return res

app.include_router(prefix="/auth", router=auth_router)
app.include_router(prefix="/api/records", router=records_router)
app.include_router(prefix="/api/users", router=user_router)
app.include_router(prefix='/api/predict', router=predictor_router)