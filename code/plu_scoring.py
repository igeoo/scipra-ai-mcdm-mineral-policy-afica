"""
P-L-U salience scoring utilities for SCIPRA.
"""

from __future__ import annotations

import re
import numpy as np


POWER_TERMS = {
    "authority", "enforcement", "mandate", "jurisdiction", "regulation",
    "capital", "investment withdrawal", "shareholding", "strike",
    "collective bargaining", "shutdown", "legal standing", "litigation",
    "injunction", "veto", "ownership", "enforcement power", "capital control",
}

LEGITIMACY_TERMS = {
    "rights", "consent", "fpic", "constitutional", "legitimacy",
    "recognition", "entitlement", "displacement", "customary", "treaty",
    "accountability", "transparency", "compliance", "environmental impact",
    "community development", "social licence", "public trust", "collective bargaining rights",
}

URGENCY_TERMS = {
    "urgency", "crisis", "strike", "displacement", "deadline", "eviction",
    "massacre", "protest", "emergency", "immediate", "overdue",
    "escalation", "moratorium", "injustice", "water contamination", "dust",
    "health impacts", "living-wage crisis", "post-massacre trauma",
}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z]{3,}", text.lower())


def count_terms(text: str, terms: set[str]) -> int:
    text_l = text.lower()
    return sum(text_l.count(term.lower()) for term in terms)


def document_frequency_scores(text: str):
    p_hits = count_terms(text, POWER_TERMS)
    l_hits = count_terms(text, LEGITIMACY_TERMS)
    u_hits = count_terms(text, URGENCY_TERMS)
    total = p_hits + l_hits + u_hits
    if total == 0:
        return {"P": 0.0, "L": 0.0, "U": 0.0}
    return {
        "P": p_hits / total,
        "L": l_hits / total,
        "U": u_hits / total,
    }


def wgi_normalise(raw_score: float) -> float:
    return float(np.clip((raw_score + 2.5) / 5.0, 0.0, 1.0))


def sic(P: float, L: float, U: float, alpha=0.30, beta=0.40, gamma=0.30) -> float:
    return alpha * P + beta * L + gamma * U


if __name__ == "__main__":
    sample = "community rights consent urgency displacement and protest"
    scores = document_frequency_scores(sample)
    print(scores)
    print("SIC:", sic(scores["P"], scores["L"], scores["U"]))
