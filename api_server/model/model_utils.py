def dummy_predict(text: str):
    if "fake" in text.lower():
        return "Fake", 0.95
    else:
        return "Real", 0.80
