import requests
import os

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

NGO_REPORTS = {
    'Bench_Marks_PG6': 'http://www.bench-marks.org.za/publications/policy_gap_6.pdf',
    'Bench_Marks_PG10': 'http://www.bench-marks.org.za/publications/policy_gap_10.pdf',
    'SERI_Marikana': 'https://www.seri-sa.org/images/Marikana_Commission_Final_Report.pdf',
    'CER_Zero_Hour': 'https://cer.org.za/wp-content/uploads/2016/05/Zero-Hour-May-2016.pdf'
}

print("--- Starting NGO Report Downloads ---")
for name, url in NGO_REPORTS.items():
    try:
        print(f"Fetching {name}...")
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            file_path = os.path.join(RAW_DIR, f"{name}.pdf")
            with open(file_path, 'wb') as f:
                f.write(r.content)
            print(f"  [SUCCESS] Saved to {file_path}")
        else:
            print(f"  [FAILED] HTTP {r.status_code}")
    except Exception as e:
        print(f"  [ERROR] {e}")

# Fetch EITI Data for South Africa
print("\n--- Fetching EITI Data ---")
EITI_URL = "https://eiti.org/api/v1.0/country_data?country=ZA&format=json"
try:
    r = requests.get(EITI_URL, timeout=15)
    if r.status_code == 200:
        file_path = os.path.join(RAW_DIR, "EITI_South_Africa.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(r.text)
        print(f"  [SUCCESS] Saved EITI data to {file_path}")
except Exception as e:
    print(f"  [ERROR] EITI: {e}")
