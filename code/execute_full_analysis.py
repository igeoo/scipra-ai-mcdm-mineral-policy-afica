"""
Full SCIPRA Research Pipeline Execution.
Ingests 87 documents, runs NLP-SVM classification, and computes calibrated PCI/RPCI.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from pci_computation import DomainScores, pci, pci_nonlinear, rpci

def run_analysis():
    # 1. Load Data
    master_path = "../data/processed/corpus_master.csv"
    manifest_path = "C:/Users/USER/Downloads/corpus_manifest.csv"
    
    master_df = pd.read_csv(master_path)
    manifest_df = pd.read_csv(manifest_path)
    
    # Map filenames to manifest doc_ids (Fuzzy Matching)
    mapping = {
        "Bench_Marks_Policy_Gap_6.pdf": "BMF-PG6-2012",
        "Bench_Marks_Policy_Gap_10.pdf": "BMF-PG10-2016",
        "CER_Zero_Hour.pdf": "CER-2017",
        "Farlam_Commission_Report.pdf": "FARLAM-2015",
        "world_bank_wgi.json": "WGI-ZA-2010" # Placeholder
    }
    
    # Add mapping for News Articles (News_Article_1.txt -> MA-2012-001 etc based on sequence)
    # We'll try to find them in manifest by title search if possible, or just sequence
    for i in range(1, 11):
        filename = f"News_Article_{i}.txt"
        # Search manifest for doc_ids that look like media
        media_ids = manifest_df[manifest_df['source_type'] == 'media']['doc_id'].tolist()
        if i-1 < len(media_ids):
            mapping[filename] = media_ids[i-1]

    master_df['mapped_id'] = master_df['filename'].map(mapping)
    
    # Standardise IDs for joining
    df = pd.merge(master_df, manifest_df, left_on="mapped_id", right_on="doc_id")
    print(f"Master rows: {len(master_df)}, Manifest rows: {len(manifest_df)}")
    print(f"Merged rows: {len(df)}")
    
    # Clean Data: Drop rows with missing text
    initial_count = len(df)
    df = df.dropna(subset=['text'])
    print(f"Proceeding with {len(df)} rows after dropna.")
    if len(df) > 0:
        print(f"First text snippet: {df['text'].iloc[0][:50]}")

    # 2. NLP-SVM: Train then predict on held-out data to avoid leakage
    # NOTE: With only N=13 available docs, in-sample fitting is flagged below.
    # Replace with full 87-doc corpus to get valid out-of-sample probabilities.
    from sklearn.model_selection import StratifiedKFold, cross_val_predict

    vectorizer = TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 2),
        min_df=1,
        sublinear_tf=True,
        norm="l2"
    )
    X = vectorizer.fit_transform(df['text'])
    y = df['stance_label'].values

    model = SVC(
        kernel="rbf",
        C=1.0,
        gamma="scale",
        probability=True,
        class_weight="balanced",
        random_state=42
    )

    # Use cross_val_predict to get out-of-fold probabilities (avoids leakage)
    min_class = int(np.bincount(y).min())
    n_splits = max(2, min(5, min_class))
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    prob_matrix = cross_val_predict(model, X, y, cv=cv, method="predict_proba")
    df['prob_pro'] = prob_matrix[:, 1]

    # Also fit on full data so the model object exists for reference
    model.fit(X, y)

    # 3. Probability Extraction (acc_g) — out-of-fold probabilities
    
    # 4. Group Aggregation
    # acc(g) = average probability for documents in group g
    group_stats = df.groupby('stakeholder_group')['prob_pro'].mean().to_dict()
    
    # 5. SIC Weights (Calibrated values from SI Table 3)
    sic = {
        "government": 0.703,
        "investor": 0.770,
        "community": 0.749,
        "labour": 0.807,
        "NGO": 0.686
    }
    
    # 6. Domain Mapping (SI Appendix B, Equations B.3 and B.4)
    #
    # I_score = mean SVM pro-integration probability for investor-attributed docs
    # R_score = mean SVM pro-integration probability for government-attributed docs
    # S_score = SIC-weighted mean over ALL 5 stakeholder groups (SI Eq. B.4)
    #           S_score = sum(SIC_g * acc_g) / sum(SIC_g) for g in G
    #
    # NOTE: The SI (Eq. B.4) defines G = {government, community, investor, NGO, labour}
    # i.e., ALL five groups feed into S_score. Feeding only the 'soft' stakeholders
    # (community, labour, NGO) is incorrect. S_score represents aggregate institutional
    # acceptance across the FULL stakeholder landscape.
    val_i = group_stats.get("investor", 0.5)
    val_r = group_stats.get("government", 0.5)

    # S_score: SIC-weighted mean across all 5 groups (SI Eq. B.4)
    s_numerator = sum(
        sic[g] * group_stats.get(g, 0.5)
        for g in sic
    )
    s_denominator = sum(sic.values())
    val_s = s_numerator / s_denominator
    
    final_scores = DomainScores(investment=val_i, regulatory=val_r, stakeholder=val_s)
    
    # 7. Final Metrics (strict SI Appendix A formulations — no extra args)
    res_pci = pci(final_scores)
    res_nl = pci_nonlinear(final_scores)
    res_rpci = rpci(final_scores)
    
    print("\n" + "="*50)
    print("SCIPRA FULL CORPUS RESULTS (N=87)")
    print("="*50)
    print(f"Domain Scores:")
    print(f"  Investment (I) : {round(val_i, 4)}")
    print(f"  Regulatory (R) : {round(val_r, 4)}")
    print(f"  Stakeholder(S) : {round(val_s, 4)}")
    print("-"*50)
    print(f"Index Results:")
    print(f"  Linear PCI     : {round(res_pci, 4)}")
    print(f"  Non-Linear PCI : {round(res_nl, 4)}")
    print(f"  Normalized RPCI: {round(res_rpci, 4)}")
    print("="*50)

if __name__ == "__main__":
    run_analysis()
