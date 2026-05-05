"""
NLP–SVM pipeline for SCIPRA stakeholder stance classification.

This script is a reproducibility scaffold. Replace the toy corpus with the
public-source Marikana corpus described in docs/DATA_ACCESS.md.
"""

from __future__ import annotations

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.metrics import cohen_kappa_score
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


RANDOM_STATE = 42


def build_tfidf(corpus: list[str]):
    vectorizer = TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 2),
        min_df=1,          # use 2 for full 87-document corpus
        max_df=0.90,
        sublinear_tf=True,
        norm="l2",
    )
    return vectorizer.fit_transform(corpus), vectorizer


def train_svm(X, y):
    model = SVC(
        kernel="rbf",
        C=1.0,
        gamma="scale",
        class_weight="balanced",
        probability=True,
        random_state=RANDOM_STATE,
    )
    # Dynamic split count to handle toy/small corpora
    min_class_size = np.min(np.bincount(y))
    n_splits = min(5, min_class_size) if min_class_size > 1 else 2
    
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=RANDOM_STATE)
    metrics = cross_validate(
        model,
        X,
        y,
        cv=cv,
        scoring=["accuracy", "precision", "recall", "f1", "roc_auc"],
    )
    model.fit(X, y)
    return model, metrics


def vader_urgency_adjustment(text: str, raw_urgency: float, ceiling: float = 0.10) -> float:
    analyzer = SentimentIntensityAnalyzer()
    compound = analyzer.polarity_scores(text)["compound"]
    return float(np.clip(raw_urgency + ceiling * compound, 0.0, 1.0))


if __name__ == "__main__":
    # Replace with cleaned Marikana corpus.
    corpus = [
        "community rights consent and participation",
        "strike crisis protest and urgent displacement",
        "regulatory compliance and transparency improved",
        "investment capital and authority mandate",
        "environmental impact and accountability",
    ]
    labels = np.array([1, 0, 1, 1, 0])

    X, vectorizer = build_tfidf(corpus)
    model, metrics = train_svm(X, labels)

    print("Features:", vectorizer.get_feature_names_out()[:10])
    print("CV metrics:", {k: v.tolist() for k, v in metrics.items()})
