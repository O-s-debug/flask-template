import requests

MODEL_API_URL = "http://127.0.0.1:8000/predict"

def send_prediction_request(text: str):
    try:
        response = requests.post(MODEL_API_URL, json={"text": text})
        if response.status_code == 200:
            return response.json()
        else:
            return {"prediction": "Error", "confidence": 0.0}
    except Exception as e:
        return {"prediction": f"Error: {str(e)}", "confidence": 0.0}
