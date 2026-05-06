import os
import pandas as pd
import pdfplumber
from docx import Document
import re
import json

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
OUTPUT_FILE = os.path.join(PROCESSED_DIR, "corpus_master.csv")

def setup_dirs():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

def clean_text(text):
    """Basic cleaning: remove multiple newlines, extra spaces, and special chars."""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_from_pdf(filepath):
    print(f"  Extracting PDF: {os.path.basename(filepath)}")
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"
    except Exception as e:
        print(f"    [ERROR] PDF Extraction failed: {e}")
    return text

def extract_from_docx(filepath):
    print(f"  Extracting Word: {os.path.basename(filepath)}")
    text = ""
    try:
        doc = Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"    [ERROR] Word Extraction failed: {e}")
    return text

def extract_from_txt(filepath):
    print(f"  Reading Text: {os.path.basename(filepath)}")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"    [ERROR] Text Read failed: {e}")
    return ""

def extract_from_json(filepath):
    print(f"  Extracting JSON: {os.path.basename(filepath)}")
    text = ""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Generic flattening for corpus inclusion
            text = json.dumps(data, indent=2)
    except Exception as e:
        print(f"    [ERROR] JSON Extraction failed: {e}")
    return text

def process_corpus():
    all_data = []
    
    supported_exts = ('.pdf', '.docx', '.txt', '.json')
    files = [f for f in os.listdir(RAW_DIR) if f.lower().endswith(supported_exts)]
    print(f"Found {len(files)} documents to process.")
    
    for filename in files:
        # Skip certain files
        if filename == "world_bank_wgi.json" and os.path.getsize(os.path.join(RAW_DIR, filename)) < 500:
            # Skip if it's the error message placeholder
            continue

        path = os.path.join(RAW_DIR, filename)
        content = ""
        
        if filename.lower().endswith('.pdf'):
            content = extract_from_pdf(path)
        elif filename.lower().endswith('.docx'):
            content = extract_from_docx(path)
        elif filename.lower().endswith('.txt'):
            content = extract_from_txt(path)
        elif filename.lower().endswith('.json'):
            content = extract_from_json(path)
            
        if content.strip():
            cleaned = clean_text(content)
            all_data.append({
                "filename": filename,
                "text": cleaned,
                "length": len(cleaned)
            })
            
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"\n[SUCCESS] Master corpus created with {len(df)} documents.")
        print(f"Saved to: {OUTPUT_FILE}")
    else:
        print("\n[WARNING] No valid text content found in documents.")

if __name__ == "__main__":
    setup_dirs()
    process_corpus()
