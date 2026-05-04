# SCIPRA — AI-Enhanced MCDM Framework for Mineral Resource Policy Convergence in Africa

> **Bridging the Investment-Regulatory-Stakeholder Divide: An AI-Enhanced MCDM Framework for Mineral Resource Policy Convergence in Africa**
>
> Ige, O.O., Mora-Camino, F., & Olanrewaju, O.A.

---

## Overview

SCIPRA is a reproducible, AI-enhanced Multi-Criteria Decision-Making (MCDM) framework designed to quantify and bridge the divide between investment, regulatory, and stakeholder interests in African mineral resource governance. The framework integrates:

- A **Policy Convergence Index (PCI)** and its robustness-adjusted form **RPCI** to measure cross-domain policy alignment
- A **Stakeholder Influence Coefficient (SIC)** derived from NLP-based salience scoring across three dimensions: Power (P), Legitimacy (L), and Urgency (U)
- An **NLP-SVM pipeline** for automated stakeholder document classification and acceptance scoring
- Empirical validation using the **Marikana case study** (North West Province, South Africa)

---

## Repository Structure

```
.
├── README.md
├── appendices/
│   └── SCIPRA_Supplementary_Material.pdf   # Full supplementary information (SI)
├── data/
│   └── ...                                 # Corpus metadata and annotation files
└── src/
    └── ...                                 # NLP-SVM pipeline scripts
```

---

## Supplementary Material

Supplementary materials are provided in:

```
appendices/SCIPRA_Supplementary_Material.pdf
```

The document contains:

| Appendix | Title | Content |
|----------|-------|---------|
| **Appendix A** | Mathematical Foundations | Formal proofs of PCI₀ ∈ [0,1] and RPCI ∈ [0,1] boundedness; monotone convergence theorem; derivation of the normalisation divisor D = 1 + λ/2; numerical verification of RPCI = 0.427, 0.638, 0.752 |
| **Appendix B** | NLP-SVM Pipeline | Complete reproducible pipeline specification: TF-IDF and salience scoring equations, Algorithms 1–3 (pseudo-code), lexicons V_P / V_L / V_U (48 terms), corpus metadata, inter-annotator agreement (κ = 0.71), and parameter calibration guidance |
| **Appendix C** | P-L-U Derivation | Step-by-step derivation of all 15 P, L, U scores for the five Marikana stakeholder groups; SIC arithmetic verification against main text Table 3; methodology transparency audit (53% Low subjectivity, 40% Low-Medium, 7% Medium) |

---

## Key Metrics

| Stakeholder Group | P | L | U | SIC |
|---|---|---|---|---|
| Government (DMRE/SAPS) | 0.82 | 0.58 | 0.75 | 0.703 |
| Nkaneng Community | 0.32 | 0.92 | 0.95 | 0.749 |
| International Investors (Lonmin/Sibanye) | 0.88 | 0.65 | 0.82 | 0.770 |
| Environmental NGOs (CER/BMF) | 0.52 | 0.80 | 0.70 | 0.686 |
| Labour Unions (AMCU/NUM) | 0.75 | 0.78 | 0.90 | 0.807 |

> SIC formula: SIC = 0.3P + 0.4L + 0.3U — all five values verified against main text Table 3.

---

## Reproducibility

Every numerical result in the main text can be independently reproduced using:

1. The equations and parameter values in **Table SI-1** (Master Symbol Reference)
2. The algorithms in **Section B.2** with settings in **Table B5.2**
3. The derivation steps in **Sections C.3–C.7** using publicly accessible sources in **Section B.4.3**

No proprietary data is required. All primary sources are cited with page-level references in the supplementary material.

**Monte Carlo validation:** P(PCI ≥ 0.70) = 99.5% across N = 10,000 iterations (σ = 5% parameter; Section 4.7, main text).

---

## Core Framework Equations

| Symbol | Definition |
|--------|------------|
| PCI₀ | Base Policy Convergence Index: PCI₀ = Σᵢ wᵢXᵢ |
| σ(X) | Weighted standard deviation: σ(X) = [Σwᵢ(Xᵢ − μ)²]^(1/2) |
| RPCI | Normalised robustness-adjusted PCI: max(0, PCI₀ − λσ(X)) / (1 + λ/2) |
| SIC | Stakeholder Influence Coefficient: SIC = αP + βL + γU |

---

## Authors

- **Ige, O.O.**
- **Mora-Camino, F.**
- **Olanrewaju, O.A.**

---

## Citation

If you use SCIPRA in your work, please cite:

```
Ige, O.O., Mora-Camino, F., & Olanrewaju, O.A. (2026). Bridging the
Investment-Regulatory-Stakeholder Divide: An AI-Enhanced MCDM Framework
for Mineral Resource Policy Convergence in Africa.
```

---

## License

Please refer to the repository license file for terms of use.
