from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import tensorflow as tf
import numpy as np

app = FastAPI()

#TODO
#model = load_model('path_to_your_model.h5')

@app.get("/")
def root():
    return {'greeting': 'Hello'}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        contents = await file.read()

        # Open the image
        image = Image.open(io.BytesIO(contents))

        # Make a prediction
        prediction = predict_image(image)
        return JSONResponse(content={"prediction": prediction})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Placeholder function for the model prediction
def predict_image(image: Image.Image) -> str:
    # For now, it returns a dummy prediction
    return "dummy_prediction"


# Below could be the code to preprocess
#def predict_image(image: Image.Image) -> str:
    # Preprocess the image to match the model input requirements
    #image = image.resize((224, 224))  # Resize the image to the input size expected by the model
    #image_array = tf.keras.preprocessing.image.img_to_array(image)
    #image_array = np.expand_dims(image_array, axis=0)  # Create batch axis
    #image_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)  # Preprocess the input as needed by the model


    #prediction = model.predict(image_array)
    #return prediction
