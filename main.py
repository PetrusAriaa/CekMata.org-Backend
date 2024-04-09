from xml.etree.ElementPath import prepare_descendant
from fastapi import FastAPI
from fastapi.applications import JSONResponse
from fastapi.exceptions import BaseModel
from routes import auth_router, records_router, user_router, predictor_router
# from dotenv import load_dotenv
from torch import nn


# load_dotenv(".env.development")

app = FastAPI()

class DummyResponse(BaseModel):
    message: str


class CNN(nn.Module):
    def __init__(self, NUMBER_OF_CLASSES):
        super(CNN, self).__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=2),
            nn.BatchNorm2d(16),
            nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(in_channels=16, out_channels=32,
                      kernel_size=3, stride=2),
            nn.BatchNorm2d(32),
            nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(in_channels=32, out_channels=64,
                      kernel_size=3, stride=2),
            nn.BatchNorm2d(64),
            nn.LeakyReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )

        self.dense_layers = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(64 * 3 * 3, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, NUMBER_OF_CLASSES),
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.dense_layers(x)

        return x

@app.get("/health", response_model=DummyResponse, tags=['HealthCheck'])
def health_check() -> JSONResponse:
    return JSONResponse({"status": "up and running"})

app.include_router(prefix="/auth", router=auth_router)
app.include_router(prefix="/records", router=records_router)
app.include_router(prefix="/users", router=user_router)
app.include_router(prefix='/predict', router=predictor_router)