from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


@dataclass
class Prediction:
    label: str
    score: float


class TinySentimentModel:
    """A tiny, offline-friendly text classifier.

    It trains quickly at container startup so the project does not
    need large model downloads.
    """

    def __init__(self) -> None:
        # Very small training set (demo only)
        pos = [
            "i love this",
            "this is awesome",
            "great work",
            "excellent result",
            "happy with the service",
            "fantastic experience",
        ]
        neg = [
            "i hate this",
            "this is terrible",
            "bad work",
            "awful result",
            "not happy",
            "horrible experience",
        ]
        X = pos + neg
        y = np.array([1] * len(pos) + [0] * len(neg))

        self._vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        Xv = self._vectorizer.fit_transform(X)

        self._clf = LogisticRegression(max_iter=200)
        self._clf.fit(Xv, y)

    def predict(self, text: str) -> Prediction:
        Xv = self._vectorizer.transform([text])
        proba_pos = float(self._clf.predict_proba(Xv)[0, 1])
        label = "positive" if proba_pos >= 0.5 else "negative"
        score = proba_pos if label == "positive" else 1.0 - proba_pos
        return Prediction(label=label, score=score)
