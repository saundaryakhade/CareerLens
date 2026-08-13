import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

def train_structured_model():
    print("\n--- Training Structured Skill Model ---")
    data_path = os.path.join(DATA_DIR, "career_prediction_dataset.csv")
    df = pd.read_csv(data_path)

    feature_cols = [c for c in df.columns if c != "career"]
    X = df[feature_cols]
    y = df["career"]

    classes = sorted(y.unique().tolist())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
    }

    results = {}
    best_name = None
    best_model = None
    best_f1 = -1.0

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted")
        cm = confusion_matrix(y_test, y_pred, labels=classes).tolist()

        results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "confusion_matrix": cm,
            "classes": classes
        }

        print(f"[{name}] Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            best_name = name
            best_model = model

    print(f"Selected Best Structured Model: {best_name} (F1: {best_f1:.4f})")
    
    # Save model and feature names
    joblib.dump({"model": best_model, "feature_names": feature_cols, "classes": classes}, os.path.join(MODELS_DIR, "career_model.joblib"))
    
    return {
        "selected_algorithm": best_name,
        "feature_count": len(feature_cols),
        "comparison": results,
        "classes": classes
    }

def train_resume_nlp_model():
    print("\n--- Training Resume NLP Model ---")
    data_path = os.path.join(DATA_DIR, "resume_career_dataset.csv")
    df = pd.read_csv(data_path)

    X = df["resume_text"]
    y = df["career"]
    classes = sorted(y.unique().tolist())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    vectorizer = TfidfVectorizer(max_features=500, stop_words="english", ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    nlp_models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
    }

    results = {}
    best_name = None
    best_model = None
    best_f1 = -1.0

    for name, model in nlp_models.items():
        model.fit(X_train_tfidf, y_train)
        y_pred = model.predict(X_test_tfidf)

        acc = accuracy_score(y_test, y_pred)
        prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted")
        cm = confusion_matrix(y_test, y_pred, labels=classes).tolist()

        results[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "confusion_matrix": cm,
            "classes": classes
        }

        print(f"[{name} NLP] Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            best_name = name
            best_model = model

    print(f"Selected Best Resume Model: {best_name} (F1: {best_f1:.4f})")

    joblib.dump(best_model, os.path.join(MODELS_DIR, "resume_model.joblib"))
    joblib.dump(vectorizer, os.path.join(MODELS_DIR, "tfidf_vectorizer.joblib"))

    return {
        "selected_algorithm": best_name,
        "vectorizer": "TF-IDF (max_features=500, ngrams=(1,2))",
        "comparison": results,
        "classes": classes
    }

def main():
    structured_metrics = train_structured_model()
    resume_metrics = train_resume_nlp_model()

    metrics = {
        "structured_model": structured_metrics,
        "resume_nlp_model": resume_metrics
    }

    metrics_path = os.path.join(MODELS_DIR, "metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nSaved training metrics to {metrics_path}")

if __name__ == "__main__":
    main()
