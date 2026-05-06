"""
Scientific Validation Tool: Compare Pure Math Outputs vs Manuscript Tables.
"""

from pci_computation import DomainScores, pci, pci_nonlinear, rpci

def validate_integrity():
    # Input data from SI Appendix C
    scenarios = {
        "Scenario A (Traditional)": (DomainScores(0.82, 0.48, 0.12), (0.30, 0.35, 0.35)),
        "Scenario B (Regulatory Emphasis)": (DomainScores(0.70, 0.75, 0.55), (0.30, 0.35, 0.35)),
        "Scenario C (SCIPRA-Optimised)": (DomainScores(0.75, 0.80, 0.79), (0.30, 0.35, 0.35)),
    }
    
    # Values EXACTLY as reported in Manuscript Table 5 & 7
    manuscript = {
        "Scenario A (Traditional)": {"pci": 0.456, "pci_nl": 0.397, "rpci": 0.427},
        "Scenario B (Regulatory Emphasis)": {"pci": 0.665, "pci_nl": 0.660, "rpci": 0.638},
        "Scenario C (SCIPRA-Optimised)": {"pci": 0.781, "pci_nl": 0.780, "rpci": 0.752},
    }

    print(f"{'Metric Validation':<35} | {'Math Output':<12} | {'Table Value':<12} | {'Delta'}")
    print("-" * 80)

    for name, (scores, weights) in scenarios.items():
        print(f"--- {name} ---")
        
        # 1. Linear PCI
        calc_pci = pci(scores, weights)
        tab_pci = manuscript[name]["pci"]
        print(f"{'Linear PCI':<35} | {calc_pci:<12.4f} | {tab_pci:<12.4f} | {calc_pci-tab_pci:+.4f}")
        
        # 2. Nonlinear PCI
        calc_nl = pci_nonlinear(scores, weights)
        tab_nl = manuscript[name]["pci_nl"]
        print(f"{'Nonlinear PCI (Harmonic-Linear)':<35} | {calc_nl:<12.4f} | {tab_nl:<12.4f} | {calc_nl-tab_nl:+.4f}")

        # 3. RPCI
        calc_rpci = rpci(scores, weights)
        tab_rpci = manuscript[name]["rpci"]
        print(f"{'Robustness PCI (Normalized)':<35} | {calc_rpci:<12.4f} | {tab_rpci:<12.4f} | {calc_rpci-tab_rpci:+.4f}")
        print("-" * 80)

if __name__ == "__main__":
    validate_integrity()
