from api_server.model.model_loader import get_model
from schemas import PredictionRequest, PredictionResponse

model = get_model()

def get_prediction(data: PredictionRequest) -> PredictionResponse:
    # Example prediction logic
    probas = model.predict_proba([data.text])[0]
    pred_index = probas.argmax()
    label = model.classes_[pred_index]
    confidence = float(probas[pred_index])

    return PredictionResponse(prediction=label, confidence=confidence)
