# Data Access Pathway

This repository uses only publicly available sources.

## 1. EITI API

Access point:
https://eiti.org/open-data

Example endpoint:
https://eiti.org/api/v1.0/?format=json&country_code=ZA

Suggested fields:
- fiscal_year
- revenue_type
- government_entity
- company_name
- amount
- currency

## 2. World Bank Worldwide Governance Indicators

Access point:
https://api.worldbank.org/v2/

Example endpoint:
https://api.worldbank.org/v2/country/ZA/indicator/GE.EST?format=json&date=2010:2023

Indicators:
- GE.EST = Government Effectiveness
- RL.EST = Rule of Law
- VA.EST = Voice and Accountability
- CC.EST = Control of Corruption
- PS.EST = Political Stability

Normalisation:
WGI_norm = (WGI_raw + 2.5) / 5.0

## 3. Farlam Commission Report

Public PDF:
https://www.gov.za/documents/marikana-commission-inquiry

Suggested extraction:
```bash
python -m pdfplumber farlam_2015.pdf --pages all > farlam_text.txt
```

## 4. NGO and civil society reports

- Bench Marks Foundation Policy Gap 6
- Bench Marks Foundation Policy Gap 10
- SERI Nkaneng report
- Centre for Environmental Rights reports

## 5. News archives

Suggested sources:
- Mining Weekly
- Engineering News
- Daily Maverick

Use scraping only where permitted by terms of use and robots.txt.
