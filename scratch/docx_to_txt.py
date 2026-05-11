import sys
import docx

def docx_to_txt(docx_path, txt_path):
    doc = docx.Document(docx_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(full_text))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python docx_to_txt.py <input.docx> <output.txt>")
    else:
        docx_to_txt(sys.argv[1], sys.argv[2])
