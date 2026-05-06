import os
import requests
import json

RAW_DIR = "data/raw"

# Updated APIs from docs/DATA_ACCESS.md
WORLD_BANK_API = "https://api.worldbank.org/v2/country/ZA/indicator/GE.EST;RL.EST;VA.EST;CC.EST;PS.EST?date=2010:2023&format=json"
EITI_API = "https://eiti.org/api/v1.0/?format=json&country_code=ZA"
FARLAM_REPORT_URL = "https://www.gov.za/sites/default/files/gcis_document/201506/marikana-report-1.pdf"

NGO_REPORTS = {
    "Bench_Marks_Policy_Gap_6": "https://www.bench-marks.org.za/wp-content/uploads/2021/02/rustenburg_review_policy_gap_final_aug_2012.pdf",
    "Bench_Marks_Policy_Gap_10": "https://www.bench-marks.org.za/wp-content/uploads/2021/02/policy_gap_10.pdf",
    "CER_Zero_Hour": "https://cer.org.za/wp-content/uploads/2016/06/Zero-Hour-May-2016.pdf"
}

def setup_dirs():
    os.makedirs(RAW_DIR, exist_ok=True)

def fetch_api_data(url, filename):
    print(f"Fetching data for {filename}...")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            with open(os.path.join(RAW_DIR, filename), "w") as f:
                json.dump(data, f, indent=4)
            print(f"  [SUCCESS] Saved {filename}.")
        else:
            print(f"  [ERROR] API returned status {response.status_code}")
    except Exception as e:
        print(f"  [ERROR] Failed to fetch {filename}: {e}")

def download_file(url, filename, force=False):
    dest = os.path.join(RAW_DIR, filename)
    if os.path.exists(dest) and not force:
        print(f"  [SKIP] {filename} already exists.")
        return

    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, stream=True, timeout=60)
        if response.status_code == 200:
            with open(dest, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"  [SUCCESS] Downloaded {filename}.")
        else:
            print(f"  [ERROR] Failed to download {filename}. Status: {response.status_code}")
    except Exception as e:
        print(f"  [ERROR] Failed to download {filename}: {e}")

if __name__ == "__main__":
    setup_dirs()
    fetch_api_data(WORLD_BANK_API, "world_bank_wgi.json")
    fetch_api_data(EITI_API, "eiti_za_data.json")
    download_file(FARLAM_REPORT_URL, "Farlam_Commission_Report.pdf")
    for name, url in NGO_REPORTS.items():
        download_file(url, f"{name}.pdf")
