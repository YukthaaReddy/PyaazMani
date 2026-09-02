# PyaazMani

PyaazMani is a smart onion quality and mandi intelligence platform built with Streamlit. It helps farmers, mandi inspectors, and government officials assess onion quality using AI-powered grading, detect diseases and pathologies, compare local mandi prices, and generate official PDF records for traceability and reporting.

## Overview

PyaazMani combines machine learning, regional mandi data, and an accessible multilingual interface into a single decision-support dashboard for onion supply chains. The platform is designed to simplify onion quality validation, reduce manual inspection effort, and provide transparent market insights for stakeholders across the agricultural ecosystem.

## Key Features

- AI-based onion grading for Grade A, Grade B, and Grade C
- Visual quality assessment with quality score and URS percentage
- Disease and pathology detection for onion health analysis
- Nearby mandi price lookup with geolocation support
- Government-exclusive official PDF report archive and record history
- Role-based access for Farmer, Mandi Quality Inspector, and Government Official
- Light and dark theme support
- multilingual interface (English, Hindi, Kannada)
- responsive layout for desktop and mobile devices
- tamper-proof record tracking with hash-based metadata

## Application Chapters

1. Check Onion Quality
   - Upload onion images or use sample data
   - Assess quality grade and confidence
   - Review disease warnings and severity

2. Nearby Mandi Prices
   - Detect user geolocation or select region
   - View nearest APMC mandis and modal prices
   - Monitor market trends and pricing data

3. Official PDF Reports & History
   - Access certified record archive
   - Search, filter, and download official reports
   - Manage tamper-proof history for government use

4. Mandi & APMC Analytics
   - Track grade distribution and volume trends
   - Visualize market performance and quality patterns

5. Settings & Display Preferences
   - Toggle light/dark mode
   - Adjust font sizing
   - Switch language and personalize user preferences

## Tech Stack

- Python
- Streamlit
- OpenCV
- NumPy
- Pandas
- scikit-learn
- Pillow
- Albumentations
- Joblib

## Project Structure

```text
onion/
│
├── README.md
├── onion grading/
│   ├── app.py
│   ├── app_backup.py
│   ├── augment_data.py
│   ├── extract_features.py
│   ├── train_model.py
│   ├── requirements.txt
│   ├── onion_model.pkl
│   ├── onionsetu.db
│   ├── data/
│   └── backend/
│       ├── ai_grader.py
│       ├── auth.py
│       ├── database.py
│       ├── disease_detector.py
│       ├── i18n.py
│       ├── ledger.py
│       ├── mandi_service.py
│       ├── pdf_generator.py
│       ├── service.py
│       └── theme.py
```

## Local Setup

### 1) Clone the repository

```bash
git clone https://github.com/YukthaaReddy/PyaazMani.git
cd PyaazMani
```

### 2) Create a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3) Install dependencies

```bash
cd "onion grading"
pip install -r requirements.txt
```

### 4) Run the app locally

```bash
python -m streamlit run app.py --server.port 8501
```

Then open the browser at:

```text
http://localhost:8501
```

You may also use port 8051 if preferred:

```bash
python -m streamlit run app.py --server.port 8051
```

## Run Notes

- The app expects the project folder to be run from the `onion grading` directory.
- If Streamlit is not recognized globally, use `python -m streamlit ...` instead of `streamlit ...`.
- The app initializes the SQLite database automatically on first run.

## License

This project is for educational and demonstration purposes and can be extended for real agricultural deployment scenarios.

## Contact

For questions, improvements, or deployment support, please connect through the project repository or the maintainer contact on the GitHub project page.
