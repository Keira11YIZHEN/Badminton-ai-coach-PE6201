"""Local badminton question classifier.

Uses TF-IDF + logistic regression to route natural-language beginner questions
into one of three bounded categories: technique, footwork, or equipment.
The split and model settings intentionally match the original A1 experiment so
reported numbers remain reproducible.
"""
from pathlib import Path
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "badminton_questions.csv"


def load_data(path=DATA_PATH):
    with open(path, encoding="utf-8") as f:
        rows=list(csv.DictReader(f))
    return rows


def make_split(rows, test_size=0.35, random_state=0):
    texts=[r["question"] for r in rows]
    labels=[r["label"] for r in rows]
    ids=[r["id"] for r in rows]
    return train_test_split(ids,texts,labels,test_size=test_size,random_state=random_state,stratify=labels)


def train_classifier(rows=None):
    rows=rows or load_data()
    ids=[r["id"] for r in rows]
    texts=[r["question"] for r in rows]
    labels=[r["label"] for r in rows]
    X_train,X_test,y_train,y_test=train_test_split(texts,labels,test_size=0.35,random_state=0,stratify=labels)
    model=make_pipeline(TfidfVectorizer(ngram_range=(1,1)),LogisticRegression(max_iter=1000))
    model.fit(X_train,y_train)
    return model,(X_train,X_test,y_train,y_test)


def predict_with_confidence(model, text):
    label=model.predict([text])[0]
    proba=model.predict_proba([text])[0]
    classes=model.named_steps['logisticregression'].classes_
    confidence=float(max(proba))
    return label, confidence, {c: float(p) for c,p in zip(classes,proba)}
