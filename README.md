# Online Retail Sales Dashboard

A Streamlit dashboard for the UCI Online Retail dataset (UK gift retailer, 1 Dec 2010 to 9 Dec 2011). It shows the main sales findings for a non-technical reader: KPIs, sales by country, monthly trend, top products and customers, key findings and a recommended action. A one-page summary is in `summary.md`.

## Setup
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
1. Download "Online Retail" from https://archive.ics.uci.edu/dataset/352/online+retail and unzip it.
2. Put `Online Retail.xlsx` in the same folder as `app.py` (or in a `data/` folder). The app finds it automatically.

## Run
```
streamlit run app.py
```

## Decisions
- The app does light cleaning only: it drops rows missing InvoiceNo, Quantity or UnitPrice, and computes Sales = Quantity x UnitPrice.
- The full analysis (duplicates, cancellations, bulk-order removal, bootstrap confidence intervals) is in the Task 1 notebook repo, so figures here can differ slightly from the notebook.
- Dataset files are not committed (22 MB); download them from UCI as above.

## Limits
One year of data, one UK retailer, many wholesale customers, 25% of rows without a customer ID, and December 2011 is a partial month.

## Related
Task 1 analysis notebook: https://github.com/varshithavarshithac345-byte/ECOMMERCE_SALES_ANALYSIS