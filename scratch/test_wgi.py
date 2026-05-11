import requests
ids = ['GE.EST', 'PV.EST', 'RL.EST', 'RQ.EST', 'CC.EST', 'VA.EST']
for id in ids:
    url = f"https://api.worldbank.org/v2/country/ZAF/indicator/{id}?format=json"
    r = requests.get(url)
    print(f"{id}: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        if isinstance(data, list) and len(data) > 1:
            print(f"  [SUCCESS] Data found for {id}")
        else:
            print(f"  [FAIL] {data[0].get('message', [{}])[0].get('value', 'No data')}")
