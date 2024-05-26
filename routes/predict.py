import io
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from PIL import Image
import onnxruntime as ort
import numpy as np


from .auth import validate_token


file_type = [
    'image/png',
    'image/jpeg',
    'image/jpg'
]

CLASSES = ['Cataract', 'Diabetic Retinopathy', 'Glaucoma', 'Normal']

predictor_router = APIRouter(tags=['Predictor'], dependencies=[Depends(validate_token)])

def prepare(byte_image):
    img = Image.open(io.BytesIO(byte_image)).resize((256,256))
    img_arr = np.array(img)
    
    if img_arr.ndim == 2:
        img_arr = np.stack([img_arr] * 3, axis=-1)
    
    img_arr = img_arr.astype(np.float32) / 255.0
    img_arr = np.transpose(img_arr, (2, 0, 1))
    img_arr = np.expand_dims(img_arr, axis=0)
    
    
    
    return img_arr


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
    
    model = ort.InferenceSession("model.onnx")
    
    try:
        ort_inputs = {model.get_inputs()[0].name: tensor}
        ort_outs = model.run(None, ort_inputs)
        index = np.array(ort_outs).argmax()
        class_name = CLASSES[index]
        return JSONResponse({'status': class_name })
    except:
        raise HTTPException(status_code=400, detail='Cannot process image data, please use different image',
                            headers={
                                "Accept": "image/jpeg, image/jpg, image/png"
                            })