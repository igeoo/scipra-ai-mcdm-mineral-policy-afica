"""
PCI and RPCI computation utilities for SCIPRA.

STRICT MATHEMATICAL IMPLEMENTATION (SI Appendix A & Section 4.5).

All formulas implement the definitions in the Supplementary Information (SI):
  - Eq. 1  (main text): Linear PCI     -> pci()
  - Eq. 6  (main text): Weighted σ     -> weighted_sigma()
  - Eq. A.10 (SI App. A): RPCI         -> rpci()
  - Sec 4.5 (main text): Non-Linear PCI -> pci_nonlinear()

The harmonic mean in pci_nonlinear() uses the WEIGHTED form (1 / sum(w_i/x_i))
to maintain internal consistency with the rest of the weighted-mean framework.
This is the theoretically defensible choice: an unweighted harmonic mean would
treat all three domains as equally important even though the paper specifies
domain weights w1=0.30, w2=0.35, w3=0.35.

RPCI: The SI defines the normalized form (Eq. A.10) as the authoritative
computational result. Table values in the manuscript should report this form.
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
    """
    Eq. 1 (main text): Standard Weighted Arithmetic Mean.
    PCI = w1*I + w2*R + w3*S
    """
    i, r, s = scores.investment, scores.regulatory, scores.stakeholder
    w1, w2, w3 = weights
    return w1 * i + w2 * r + w3 * s


def weighted_sigma(scores: DomainScores, weights=(0.30, 0.35, 0.35)) -> float:
    """
    Eq. 6 (main text): Weighted standard deviation across domains.
    sigma(X) = sqrt( sum_i( w_i * (X_i - mu)^2 ) )
    Bounded in [0, 0.5] per Lemma A.1.1 (SI Appendix A).
    """
    values = [scores.investment, scores.regulatory, scores.stakeholder]
    mu = sum(w * x for w, x in zip(weights, values))
    var = sum(w * (x - mu) ** 2 for w, x in zip(weights, values))
    return math.sqrt(var)


def rpci_raw(scores: DomainScores, weights=(0.30, 0.35, 0.35), lam=0.10) -> float:
    """
    Eq. 5 (main text): Un-normalized RPCI before the SI normalization step.
    RPCI_raw = max(0, PCI0 - lambda * sigma(X))

    NOTE: The manuscript Remark in Section 3.3 cites the values 0.427, 0.638,
    0.752 — these correspond to this RAW form, not the normalized form.
    This accessor is retained for reference and manuscript cross-checking only.
    The authoritative computational form is rpci() below.
    """
    base = pci(scores, weights)
    sig = weighted_sigma(scores, weights)
    return max(0.0, base - (lam * sig))


def rpci(scores: DomainScores, weights=(0.30, 0.35, 0.35), lam=0.10) -> float:
    """
    Eq. A.10 (SI Appendix A): Normalized Robustness-adjusted PCI.
    RPCI = max(0, PCI0 - lambda*sigma(X)) / (1 + lambda/2)

    This is the DEFINITIVE computational form per SI Section A.4.2, Step 4.
    Eq. 8 in the main text is a shorthand multiplicative representation of
    this same formula; both produce identical numerical results (SI Section A.1.3).

    The normalization divisor D = 1 + lambda/2 is derived from the range of
    RPCI_raw in [–lambda/2, 1] — it is the unique linear scaling that:
      (i)  maps RPCI to [0, 1], and
      (ii) preserves strict monotone ordering (Theorem A.2, SI Appendix A).
    """
    raw = rpci_raw(scores, weights, lam)
    return raw / (1.0 + lam / 2.0)


def pci_nonlinear(scores: DomainScores, weights=(0.30, 0.35, 0.35), beta=0.5) -> float:
    """
    Section 4.5 (main text): Nonlinear Policy Convergence Index.
    Universal Harmonic-Linear Blend: PCI_NL = beta*PCI_lin + (1-beta)*HM

    The harmonic mean uses the WEIGHTED form for consistency with the rest
    of the SCIPRA framework's weighted combination approach:
      HM_w = 1 / sum(w_i / X_i)

    This differs from the simple unweighted harmonic mean (n / sum(1/x)) used
    in some interpretations; the weighted form is theoretically preferred because
    it honours the domain-weight structure w1=0.30, w2=0.35, w3=0.35.

    Edge case: if any domain score is zero or negative, the harmonic mean is
    undefined; the function returns the linear PCI as a safe fallback.
    """
    values = [scores.investment, scores.regulatory, scores.stakeholder]
    p_lin = pci(scores, weights)

    # Weighted harmonic mean: HM_w = 1 / sum(w_i / x_i)
    if any(x <= 0 for x in values):
        # Harmonic mean undefined for non-positive inputs; fall back to linear.
        p_harm = p_lin
    else:
        p_harm = 1.0 / sum(w / x for w, x in zip(weights, values))

    return beta * p_lin + (1.0 - beta) * p_harm


if __name__ == "__main__":
    # Marikana domain scores derived from SI Appendix C (Table C8.2 SIC cross-check)
    # and reported in manuscript Table 5.
    scenarios = {
        "A": DomainScores(0.82, 0.48, 0.12),   # Pre-Intervention (2010-2012)
        "B": DomainScores(0.70, 0.75, 0.55),   # Post-Charter III (2018-2021)
        "C": DomainScores(0.75, 0.80, 0.79),   # SCIPRA-Optimised (projected)
    }

    header = f"{'Scenario':<25} {'PCI':>8} {'PCI-NL':>10} {'RPCI(raw)':>12} {'RPCI(norm)':>12}"
    print("SCIPRA Pure Mathematical Model (Strict SI Alignment)")
    print("=" * len(header))
    print(header)
    print("-" * len(header))
    for name, sc in scenarios.items():
        print(
            f"Scenario {name:<16}"
            f" {pci(sc):>8.4f}"
            f" {pci_nonlinear(sc):>10.4f}"
            f" {rpci_raw(sc):>12.4f}"
            f" {rpci(sc):>12.4f}"
        )
    print("=" * len(header))
    print()
    print("NOTE: Manuscript tables should report RPCI(norm) per SI Eq. A.10.")
    print("      RPCI(raw) is retained for cross-reference with Section 3.3 Remark.")
