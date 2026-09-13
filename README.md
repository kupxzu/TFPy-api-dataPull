"# TFPy-api-dataPull" 

--- install
pip install requests pandas tensorflow

--- run
python main.py

##### notes
1. i added api json auto exportation just for future project aheads(legacy pin point)
2. created a this predictive analysis to help our hospital to detairmain the increasing sicknesses

(This system pulls historical patient logs, runs linear regression trend forecasting using TensorFlow, automatically assesses outbreak risk levels, and generates dynamic clinical action plans for Chief Nurses and hospital administrators.)
---
## Key Features

* **Live Laravel API Sync:** Automatically fetches real-time disease records from the hospital backend (`/api/diseases`).
* **TensorFlow Trend Analytics:** Computes **Trend Slopes** and calculates **Next Week Case Forecasts** ($y = mx + b$).
* **Dynamic Clinical Keyword Engine:** Categorizes diseases across 8 medical domains (Respiratory, Vector-borne, Gastrointestinal, Cardiovascular, Metabolic, Neurological, Dermatological, Pediatric/Geriatric).
* **Volatility & Risk Scoring:** Detects sudden case spikes using Standard Deviation analysis to flag High-Volatility events.
* **Chief Nurse Dashboard UI:** Auto-generates an HTML dashboard (`chief_nurse_dashboard.html`) styled with TailwindCSS for immediate clinical decision-making.
* **JSON Microservice Export:** Exports all model outputs, time-series data, and dynamic advisories to `data.json` for integration with external dashboards, mobile apps, or reporting tools.

## Prerequisites & Installation

Ensure you have **Python 3.9+** installed. Install all required dependencies using `pip`:


aggregation
Laravel API Data to (Raw Json) ---> aggregate.py(Weekly Counts Array) ---> predict.py(TensorFlow) to main ---> Forecast to Chief Nurse Dashboard