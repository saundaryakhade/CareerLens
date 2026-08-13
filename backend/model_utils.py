import os
import joblib
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")

CAREER_MODEL_PATH = os.path.join(MODELS_DIR, "career_model.joblib")
RESUME_MODEL_PATH = os.path.join(MODELS_DIR, "resume_model.joblib")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib")
METRICS_PATH = os.path.join(MODELS_DIR, "metrics.json")

_career_model_obj = None
_resume_model_obj = None
_tfidf_vectorizer_obj = None

def get_career_model():
    global _career_model_obj
    if _career_model_obj is None:
        if not os.path.exists(CAREER_MODEL_PATH):
            raise FileNotFoundError(f"Model file missing: {CAREER_MODEL_PATH}. Run train_model.py first.")
        _career_model_obj = joblib.load(CAREER_MODEL_PATH)
    return _career_model_obj

def get_resume_model_and_vectorizer():
    global _resume_model_obj, _tfidf_vectorizer_obj
    if _resume_model_obj is None or _tfidf_vectorizer_obj is None:
        if not os.path.exists(RESUME_MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
            raise FileNotFoundError("Resume model files missing. Run train_model.py first.")
        _resume_model_obj = joblib.load(RESUME_MODEL_PATH)
        _tfidf_vectorizer_obj = joblib.load(VECTORIZER_PATH)
    return _resume_model_obj, _tfidf_vectorizer_obj

def predict_career_from_skills(user_skills):
    model_data = get_career_model()
    model = model_data["model"]
    feature_names = model_data["feature_names"]
    classes = model_data["classes"]

    # Normalize user skills (case insensitive match)
    user_skills_lower = {s.strip().lower() for s in user_skills}
    
    vector = []
    for feat in feature_names:
        val = 1 if feat.lower() in user_skills_lower else 0
        vector.append(val)

    import pandas as pd
    vector_df = pd.DataFrame([vector], columns=feature_names)
    probabilities = model.predict_proba(vector_df)[0]
    
    prob_dict = {}
    for idx, cls_name in enumerate(classes):
        prob_dict[cls_name] = round(float(probabilities[idx]) * 100, 2)

    # Sort probabilities descending
    sorted_probs = dict(sorted(prob_dict.items(), key=lambda item: item[1], reverse=True))
    
    top_career = list(sorted_probs.keys())[0]
    top_confidence = sorted_probs[top_career]

    return {
        "predicted_career": top_career,
        "confidence": top_confidence,
        "probabilities": sorted_probs,
        "encoded_vector": vector
    }

def predict_career_from_resume_text(text):
    model, vectorizer = get_resume_model_and_vectorizer()
    classes = model.classes_.tolist()

    text_vector = vectorizer.transform([text])
    probabilities = model.predict_proba(text_vector)[0]

    prob_dict = {}
    for idx, cls_name in enumerate(classes):
        prob_dict[cls_name] = round(float(probabilities[idx]) * 100, 2)

    sorted_probs = dict(sorted(prob_dict.items(), key=lambda item: item[1], reverse=True))

    top_career = list(sorted_probs.keys())[0]
    top_confidence = sorted_probs[top_career]

    return {
        "predicted_career": top_career,
        "confidence": top_confidence,
        "probabilities": sorted_probs
    }

def get_model_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"error": "Metrics file not found. Train model first."}
