import joblib

# Load your model at startup
model = joblib.load("models/model_file.pkl")

def get_model():
    return model
