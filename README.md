# Oil Well Production Forecasting Dashboard

A petroleum-data analytics project for analysing historical oil-well production,
identifying decline trends, and generating short-term production forecasts.

## Features
- Well-wise historical oil production analysis
- Gas-rate, water-cut, and uptime monitoring
- Exponential-decline baseline forecasting
- 3–24 month forecast horizon
- Interactive Streamlit dashboard
- Power BI-ready CSV dataset
- Reproducible synthetic demo data

## Technology
Python, Pandas, NumPy, Scikit-learn, Plotly, Streamlit, Power BI

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dataset
`data/sample_production.csv` contains synthetic monthly records for three wells
from 2022–2025. It is intentionally synthetic so the repository can be public.

## Power BI
Import `data/sample_production.csv` into Power BI to create production trends,
well comparisons, water-cut analysis, decline indicators, and forecast visuals.

## Limitation
The forecasting model is an educational exponential-decline baseline, not a
calibrated reservoir-engineering forecast. Real deployment requires validated
production history, operational events, reservoir information, and engineering review.
