import io
from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import torchvision.transforms as transforms
import torch


from .auth import validate_token


predictor_router = APIRouter(tags=['Predictor'], dependencies=[Depends(validate_token)])

model = torch.jit.load('cekmata_model.pt')

def prepare(byte_image):
    trf = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize(256),
    ])
    
    img = Image.open(io.BytesIO(byte_image))
    return trf(img).unsqueeze(0)


@predictor_router.post('')
def predict(file: UploadFile = File(...)):
    img = file.file.read()
    tensor = prepare(img)
    
    class_name = 'None'
    with torch.no_grad():
        model.eval()
        output =model(tensor)
        index = output.data.cpu().numpy().argmax()
        classes = ['Cataract', 'Diabetic Retinopathy', 'Glaucoma', 'Normal']
        class_name = classes[index]
    
    return JSONResponse({'status': class_name})