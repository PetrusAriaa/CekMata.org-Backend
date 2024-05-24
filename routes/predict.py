import io
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from PIL import Image
import torchvision.transforms as transforms
import torch


from .auth import validate_token


file_type = [
    'image/png',
    'image/jpeg',
    'image/jpg'
]

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
def predict(file: UploadFile):
    try:
        file_type.index(file.content_type)
    except ValueError :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Cannot process wrong file format. Please send these type of file format: [jpeg/jpg/png]',
                            headers={
                                "Accept": "image/jpeg, image/jpg, image/png"
                            })
    img = file.file.read()
    tensor = prepare(img)
    
    class_name = 'None'
    try:
        with torch.no_grad():
            model.eval()
            output =model(tensor)
            index = output.data.cpu().numpy().argmax()
            classes = ['Cataract', 'Diabetic Retinopathy', 'Glaucoma', 'Normal']
            class_name = classes[index]
        return JSONResponse({'status': class_name})
    except:
        raise HTTPException(status_code=400, detail='Cannot process image data, please use different image',
                            headers={
                                "Accept": "image/jpeg, image/jpg, image/png"
                            })