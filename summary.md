# SUMMARY.md

## Key Takeaways 💡

1. **Dynamic Interactive Analytics**: Developed a full-featured Streamlit sales dashboard that dynamically filters analytics based on user-selected countries. Key metrics—including **Total Sales (£)**, **Total Orders**, **Units Sold**, and **Average Order Value (£)**—recalculate in real-time.
2. **Resilient Data Auto-Detection**: Implemented intelligent data-loading logic using `os.path` and `glob` to auto-detect `Online Retail.xlsx` (or `.csv`) across project folders and environment paths, resolving path mismatch errors gracefully.
3. **Multi-Dimensional Visualizations & Insights**: Integrated interactive Plotly horizontal bar charts to highlight **Top 10 Best-Selling Products** by volume and **Top 10 Countries** by revenue, complete with automated dynamic text summaries highlighting top performers.

---

## Recommended Action 🚀

* **Deploy to Streamlit Cloud**: Package the project with a `requirements.txt` file containing `streamlit`, `pandas`, `openpyxl`, and `plotly`. Push the project directory to GitHub and connect it to Streamlit Community Cloud for free, web-accessible dashboard distribution.

---

## Final Reproducibility Check 🔄

To run this dashboard on any clean machine, confirm the following steps:

| Step | Task | Command / Check |
| :--- | :--- | :--- |
| **1. Prerequisites** | Ensure Python 3.9+ is installed | `python --version` |
| **2. Dependencies** | Install required libraries | `pip install streamlit pandas openpyxl plotly` |
| **3. Project Files** | Verify `app.py` and `Online Retail.xlsx` are in the same folder | `C:\Users\...\ecommerce_sales_project\` |
| **4. Execution** | Launch the Streamlit web application | `streamlit run app.py` |
| **5. Verification** | Open browser at local address | Access `http://localhost:8501` |