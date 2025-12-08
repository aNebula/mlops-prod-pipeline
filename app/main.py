
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
from prometheus_fastapi_instrumentator import Instrumentator
app = FastAPI(
    title="Production ML Model API",
    description="An API for serving a Scikit-learn model, deployed via a Git-driven MLOps pipeline.",
    version="1.0.0",
)
# This line automatically adds a /metrics endpoint for Prometheus to scrape
Instrumentator().instrument(app).expose(app)
# Pydantic model for input validation and API documentation
class ModelInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# The model is loaded from a local filesystem path within the container.
# The CI/CD pipeline is responsible for "baking" the correct model artifacts
# into this path during the Docker image build process.
MODEL_PATH = "./model"
print(f"Loading model from path: {MODEL_PATH}...")
# What is mlflow.pyfunc, you ask? https://mlflow.org/docs/latest/ml/traditional-ml/tutorials/creating-custom-pyfunc/part2-pyfunc-components/
model = mlflow.pyfunc.load_model(MODEL_PATH)
print("Model loaded successfully into memory.")

@app.post("/predict", tags=["Prediction"])
def predict(data: ModelInput):
    """Makes a prediction based on the input data."""
    input_df = pd.DataFrame([data.dict()])
    prediction = model.predict(input_df)
    return {"prediction": prediction.tolist()}

@app.get("/health", tags=["Health Check"])
def health_check():
    """Simple health check endpoint to confirm the API is running."""
    return {"status": "ok"}