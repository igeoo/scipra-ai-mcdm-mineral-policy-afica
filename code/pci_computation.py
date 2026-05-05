"""
PCI and RPCI computation utilities for SCIPRA.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class DomainScores:
    investment: float
    regulatory: float
    stakeholder: float


def pci(scores: DomainScores, weights=(0.30, 0.35, 0.35)) -> float:
    i, r, s = scores.investment, scores.regulatory, scores.stakeholder
    w1, w2, w3 = weights
    return w1 * i + w2 * r + w3 * s


def weighted_sigma(scores: DomainScores, weights=(0.30, 0.35, 0.35)) -> float:
    values = [scores.investment, scores.regulatory, scores.stakeholder]
    mu = sum(w * x for w, x in zip(weights, values))
    var = sum(w * (x - mu) ** 2 for w, x in zip(weights, values))
    return math.sqrt(var)


def rpci(scores: DomainScores, weights=(0.30, 0.35, 0.35), lam=0.10, normalised=True) -> float:
    base = pci(scores, weights)
    sig = weighted_sigma(scores, weights)
    raw = max(0.0, base - lam * sig)
    if normalised:
        return raw / (1 + lam / 2)
    return raw


if __name__ == "__main__":
    scenarios = {
        "A_Pre_intervention": DomainScores(0.82, 0.48, 0.12),
        "B_Post_Charter_III": DomainScores(0.70, 0.75, 0.55),
        "C_SCIPRA_optimised": DomainScores(0.75, 0.80, 0.79),
    }

    for name, scores in scenarios.items():
        print(name)
        print("  PCI:", round(pci(scores), 3))
        print("  sigma:", round(weighted_sigma(scores), 3))
        print("  RPCI raw:", round(rpci(scores, normalised=False), 3))
        print("  RPCI normalised:", round(rpci(scores, normalised=True), 3))
