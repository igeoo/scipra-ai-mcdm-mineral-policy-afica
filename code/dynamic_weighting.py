"""
Dynamic Stakeholder Salience Mapping for SCIPRA.
Implements the Stakeholder Influence Coefficient (SIC) and weight adjustment.
"""

import numpy as np

def calculate_sic(P, L, U, alpha=0.3, beta=0.4, gamma=0.3):
    """
    Equation 2: SIC = alpha*P + beta*L + gamma*U
    Reflects the weighted salience of a stakeholder.
    """
    return alpha * P + beta * L + gamma * U

def adjust_weights(W0, SIC, delta=0.3):
    """
    Equation 3: Wa = W0 * (1 + delta * SIC)
    Adjusts base AHP weights based on stakeholder influence.
    Note: The result should be normalized so that sum(Wa) = 1.
    """
    Wa_raw = W0 * (1 + delta * SIC)
    return Wa_raw / np.sum(Wa_raw)

if __name__ == "__main__":
    # Example from Marikana Case (Manuscript Table 3 & 4)
    # Community: P=0.32, L=0.92, U=0.95
    community_sic = calculate_sic(0.32, 0.92, 0.95)
    print(f"Community SIC: {community_sic:.3f}")
    
    # Base weights for a specific regulatory criterion
    # e.g., Local Employment vs Environmental Compliance
    W0 = np.array([0.15, 0.15]) 
    Wa = adjust_weights(W0, community_sic)
    print(f"Adjusted Weights: {Wa}")
