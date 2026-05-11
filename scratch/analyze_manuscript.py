from docx import Document
import os

doc_path = 'appendices/SCIPRA_Supplementary_Material.docx'
output_path = 'manuscript_analysis.txt'

if os.path.exists(doc_path):
    doc = Document(doc_path)
    # Search for keywords related to data collection and processing
    keywords = ['document', 'corpus', 'SVM', 'TF-IDF', 'Marikana', 'classification', 'processing', 'extraction']
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("--- APPENDIX END ---\n\n")
        for p in doc.paragraphs[200:]:
            f.write(p.text + "\n")
    print(f"Analysis saved to {output_path}")
else:
    print(f"File {doc_path} not found.")
