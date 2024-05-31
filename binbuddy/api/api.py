from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import tensorflow as tf
import numpy as np
from binbuddy.ml_logic.registry import load_model
import json

app = FastAPI()

# Load the model
app.state.model = load_model()

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

        return prediction_to_json(prediction)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def predict_image(image: Image.Image) -> str:
    # Preprocess the image to match the model input requirements
    image = image.resize((150, 150))  # Resize the image to the input size expected by the model
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)  # Create batch axis

    # Make prediction
    prediction = app.state.model.predict(image_array)

    return prediction

def prediction_to_json(prediction) -> JSONResponse:
    """
    Converts a model prediction to a JSON response.

    This function takes the prediction output from a machine learning model,
    identifies the class with the highest probability, and formats this
    information into a JSON response.

    Args:
        prediction (numpy.ndarray): A 2D numpy array containing the model's
            prediction probabilities for each class. The array is expected
            to have the shape (1, number_of_classes).

    Returns:
        JSONResponse: A FastAPI JSONResponse containing the predicted class
        name and its corresponding probability score.

    Example:
        prediction = model.predict(image_array)
        response = prediction_to_json(prediction)
        # response will be a JSON response like:
        # {
        #   "prediction": "biological",
        #   "score": 0.9940943121910095
        # }
    """
    # Define class names
    class_names = ['biological', 'glass', 'paper', 'plastic', 'trash']

    # Get the highest probability and corresponding class
    max_index = np.argmax(prediction[0])
    class_name = class_names[max_index]
    score = prediction[0][max_index]

    # Format the result
    result = {
        "prediction": class_name,
        "score": float(score)
    }

    # Return JSON response
    return JSONResponse(content=result)
