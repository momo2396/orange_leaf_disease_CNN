from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
import requests
from io import BytesIO
from PIL import Image
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

# model = tf.keras.models.load_model("../saved_models/2/orange_leaf_disease_prediction_model_keras.keras")

endpoint = "http://localhost:8501/v1/models/orange_leaf_disease_models:predict"

class_names = ['Citrus Canker Diseases Orange Leaf',
'Citrus Nutrient Deficiency Yellow Orange Leaf',
'Healthy Orange Leaf',
'Multiple Diseases Orange Leaf',
'Young Healthy Orange Leaf']

def read_file_as_image(data)  -> np.ndarray:
    image = Image.open(BytesIO(data))
    image = image.resize((128, 128), Image.Resampling.LANCZOS)
    image = np.array(image)
    return image

@app.get("/ping")
async def ping():
    return "Hello, I am alive..."

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    image_batch = np.expand_dims(image, 0)

    json_data = {
        "instances": image_batch.tolist()
    }

    response = requests.post(endpoint, json= json_data)
    # print(response)
    # pass
    # prediction = np.array(response.json()["predictions"][0])

    # predicted_class = np.argmax(prediction)
    # confidence = np.max(prediction)
    predictions = response.json()['predictions']
    predicted_class_idx = np.argmax(predictions[0])
    predicted_class = class_names[predicted_class_idx]
    confidence = float(np.max(predictions[0]))
    # prediction = model.predict(image_batch)
    # index = np.argmax(prediction[0])
    # predicted_class = class_names[index]
    # confidence = np.max(prediction[0])
    return {
        'Class_Name': predicted_class,
        'Confidence' : float(confidence)
    }

if __name__ == "__api__":
    uvicorn.run(app, host = 'localhost', port = 8000)