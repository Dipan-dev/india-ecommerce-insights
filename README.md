# E-Commerce Sales Analysis 🛒📊

**A complete end-to-end Data Analyst project** covering data generation, SQL analysis, Python visualizations, and an executive dashboard — built for an Indian e-commerce business (Jan–Dec 2023).

---

## Project Structure

```
ecommerce-sales-analysis/
│
├── data/
│   ├── generate_data.py       # Synthetic dataset generator
│   ├── orders.csv             # 3,000 order records
│   └── customers.csv          # 500 customer records
│
├── sql/
│   └── analysis_queries.sql   # 10 business SQL queries
│
├── visualizations/
│   ├── 01_monthly_revenue_trend.png
│   ├── 02_category_revenue.png
│   ├── 03_order_status_donut.png
│   ├── 04_city_revenue.png
│   ├── 05_payment_methods.png
│   ├── 06_customer_segments.png
│   ├── 07_discount_impact.png
│   └── 08_executive_dashboard.png
│
├── reports/
│   └── insights_report.md     # Written business insights
│
├── analysis.py                # Main Python analysis script
└── README.md
```

---

## Dataset Overview

| Attribute        | Details                              |
|------------------|--------------------------------------|
| Time Period      | January 2023 – December 2023         |
| Total Orders     | 3,000                                |
| Customers        | 500                                  |
| Product Categories | Electronics, Clothing, Home & Kitchen, Books, Sports, Beauty |
| Cities Covered   | 10 major Indian cities               |
| Payment Methods  | UPI, Credit Card, Debit Card, Net Banking, COD |

---

## Key Business Questions Answered

1. What is the overall revenue, order volume, and average order value?
2. How does revenue trend month-over-month across 2023?
3. Which product categories drive the most revenue?
4. Which cities are the top performers in sales?
5. What is the order cancellation and return rate?
6. Which payment methods do customers prefer?
7. How are customers segmented by purchase frequency (RFM)?
8. Does offering discounts actually increase or decrease revenue?
9. What share of customers are repeat buyers vs one-time buyers?
10. What is the revenue impact of returns and cancellations?

---

## Key Insights

- **Total Revenue**: ₹44.02 Lakhs from 2,338 delivered orders
- **Top Category**: Electronics leads all categories in revenue
- **Return Rate**: 8.4% — within acceptable industry range
- **UPI Dominance**: Most preferred payment method
- **Customer Retention**: Majority are one-time buyers — loyalty program opportunity
- **Discount Sweet Spot**: Medium discounts (11–20%) drive highest avg order value

---

## Tech Stack

| Tool       | Purpose                         |
|------------|---------------------------------|
| Python 3   | Data analysis & visualizations  |
| Pandas     | Data manipulation               |
| Matplotlib | Charts & dashboard              |
| NumPy      | Numerical operations            |
| SQL (SQLite compatible) | Business queries    |

---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/Dipan-dev/ecommerce-sales-analysis.git
cd ecommerce-sales-analysis

# 2. Install dependencies
pip install pandas numpy matplotlib

# 3. Generate dataset
python data/generate_data.py

# 4. Run full analysis + generate all charts
python analysis.py
```

---

## Dashboard Preview

![Executive Dashboard](visualizations/08_executive_dashboard.png)

---

## 👤 Author

**Dipan Shil** — Business Analyst | Data Enthusiast  
[LinkedIn](https://linkedin.com/in/dipanshil) • [GitHub](https://github.com/Dipan-dev)

---

> *This project uses synthetically generated data modelled on realistic Indian e-commerce patterns. No real customer data is used.*
