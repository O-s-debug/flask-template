from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import PredictionRequest, PredictionResponse
from model.model_utils import dummy_predict

app = FastAPI(title="Model API")

# Allow access from Flask frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in production use ["http://localhost:5000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FastAPI model API is running."}

@app.post("/predict", response_model=PredictionResponse)
def predict_text(request: PredictionRequest):
    prediction, confidence = dummy_predict(request.text)
    return PredictionResponse(prediction=prediction, confidence=confidence)
