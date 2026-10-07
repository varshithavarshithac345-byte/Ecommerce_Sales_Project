# Ecommerce Sales Dashboard

A Streamlit dashboard for the UCI Online Retail dataset (UK gift retailer, 1 Dec 2010 to 9 Dec 2011). It answers three questions for a non-technical reader and includes a one-page summary (see `summary.md`).

## Questions
1. Which products and countries drive revenue, and how concentrated is it?
2. Is the Q4 spike seasonality or growth?
3. How much revenue comes from repeat vs one-time customers?

## Setup
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
1. Download "Online Retail" from https://archive.ics.uci.edu/dataset/352/online+retail and unzip it.
2. Generate the cleaned data by running the analysis notebook (see the Task 1 repo, link below). It saves `clean_retail.csv`.
3. Put `clean_retail.csv` where `app.py` expects it.

## Run
```
streamlit run app.py
```

## Key decisions
- Removed duplicates, cancellations, non-positive quantity or price, and non-product codes.
- Removed two bulk orders (74k and 81k units) cancelled the same day, because they inflated product revenue.
- Kept rows with no CustomerID for Questions 1 and 2; excluded them from Question 3 (25% of rows).
- Uncertainty is shown as 95% bootstrap intervals.
- December 2011 is a partial month (data ends 9 Dec) and is greyed out.

## Findings
- Top 20% of products = 78.3% of revenue; UK = 84.8% of revenue.
- Sep to Nov = 37.5% of 12-month revenue; 1-9 Dec 2011 is 9.3% above 2010.
- Repeat customers = 65.3% of customers and 93.5% of revenue.

## Limits
One year of data, one UK retailer, many wholesale customers, and 25% of rows without a customer ID.

## Related
Task 1 analysis notebook: PASTE-YOUR-TASK-1-REPO-LINK-HERE