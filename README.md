<div align="center">

<br/>

<h1>Q - C O M M E R C E &nbsp; A N A L Y T I C S</h1>
<sub>— &nbsp; G R O C E R Y  O R D E R  I N T E L L I G E N C E  P I P E L I N E &nbsp; —</sub>

<br/><br/>

![Status](https://img.shields.io/badge/STATUS-COMPLETE-217346?style=for-the-badge&labelColor=000000)
![Dataset](https://img.shields.io/badge/DATASET-32M_INSTACART_LINE_ITEMS-217346?style=for-the-badge&labelColor=000000)
![MySQL](https://img.shields.io/badge/MySQL-SQL_Engine-217346?style=for-the-badge&logo=mysql&labelColor=000000&logoColor=217346)
![Python](https://img.shields.io/badge/PYTHON-3.12-217346?style=for-the-badge&logo=python&labelColor=000000&logoColor=217346)
![PowerBI](https://img.shields.io/badge/Power_BI-DAX_%26_Python-217346?style=for-the-badge&logo=powerbi&labelColor=000000&logoColor=217346)

<br/>

</div>

---

  <div>
    <img src="https://raw.githubusercontent.com/Muntasirzx/-Instacart-Q-Commerce-Analytics-using-SQL-and-PowerBI/refs/heads/main/Data/Adobe%20Express%20-%2020.04.2026_02.40.30_REC.gif" width="49%"/>
    <img src="https://raw.githubusercontent.com/Muntasirzx/-Instacart-Q-Commerce-Analytics-using-SQL-and-PowerBI/refs/heads/main/Data/%7BCBA30961-B7DF-41DC-9A90-F7C575ADBC0F%7D.png" width="49%"/>
  </div>


  
---

## `〉` Overview

This project is a full-stack analytics pipeline built on the public Instacart Market Basket dataset — approximately **3.4 million orders** and **32 million individual line items** across 206,209 customers.

The pipeline addresses three operational domains relevant to quick-commerce: staffing and logistics optimization, customer segmentation, and inventory placement strategy. It traverses four sequential stages: SQL extraction, MySQL-native EDA and validation, Power BI dashboarding, and Python statistical visualizations embedded directly into the BI canvas.

---

## `〉` Business Objectives

<br/>

| Domain | Objective |
|---|---|
| **Operations** | Identify peak order hours by department to inform dark-store staffing schedules and driver routing |
| **Marketing** | Segment customers by purchasing behavior (Recency, Frequency, Volume) to support retention targeting |
| **Inventory** | Analyze product reorder rates and item affinities to determine warehouse placement priorities |

<br/>

---

## `〉` Dataset & Schema

Source: [Instacart Market Basket Analysis — Kaggle](https://www.kaggle.com/c/instacart-market-basket-analysis)

| Table | Rows | Key Columns |
|---|---|---|
| `orders` | 3,421,083 | `order_id`, `user_id`, `order_dow`, `order_hour_of_day`, `days_since_prior_order` |
| `order_products` | 32,000,000+ | `order_id`, `product_id`, `add_to_cart_order`, `reordered` |
| `products` | 49,688 | `product_id`, `product_name`, `aisle_id`, `department_id` |
| `departments` | 21 | `department_id`, `department` |
| `aisles` | 134 | `aisle_id`, `aisle` |
| `dim_customers` | derived | Aggregated user dimensions for analytical mapping |

---

## `〉` Pipeline Architecture

```
┌───────────────────────────────────────────────────────────────────┐
│           Q-COMMERCE ANALYTICS PIPELINE                           │
├──────────────────┬────────────────────────────────────────────────┤
│  PHASE 1         │  MySQL                                         │
│  SQL Extraction  │  Window functions · Self-joins · CTEs          │
│                  │  Aggregated views exported as .csv extracts    │
├──────────────────┼────────────────────────────────────────────────┤
│  PHASE 2         │  MySQL                                         │
│  EDA & Validation│  Null profiling · Outlier detection            │
│                  │  Referential integrity checks across 6 tables  │
├──────────────────┼────────────────────────────────────────────────┤
│  PHASE 3         │  Power BI (Import Mode)                        │
│  BI Dashboard    │  Kimball Star Schema · DAX KPI measures        │
│                  │  Heatmaps · Donut · Matrix · Slicers           │
├──────────────────┼────────────────────────────────────────────────┤
│  PHASE 4         │  Python (Matplotlib · Seaborn)                 │
│  Statistical Viz │  Ridge plot (hourly demand by department)      │
│                  │  Violin plot (frequency distribution by tier)  │
└──────────────────┴────────────────────────────────────────────────┘
```

---

## `〉` Platform KPIs

Extracted via MySQL from the full dataset:

| Metric | Value |
|---|---|
| Total Orders | 3,421,083 |
| Total Customers | 206,209 |
| Average Basket Size | 10.09 items |
| Global Reorder Rate | 58.97% |

---

## `〉` File Structure

```
qcommerce-analytics/
├── data/                                  # Raw Kaggle CSVs (not committed)
├── sql/
│   ├── 00_eda_data_validation.sql         # Null checks, outlier detection, integrity
│   ├── 01_core_kpis.sql                   # Baseline metrics
│   ├── 02_customer_segmentation.sql       # RFV classification & window functions
│   ├── 03_department_reorders.sql         # Departmental reorder rates
│   ├── 04_temporal_logistics.sql          # Heatmap base data
│   └── 05_market_basket.sql               # Product affinity self-joins
├── python/
│   ├── 01_purchasing_rhythm.py            # Ridge plot (Matplotlib / Seaborn)
│   └── 02_habit_engine.py                 # Violin plot customer distributions
├── powerbi/
│   └── Instacart_Dashboard.pbix           # Interactive dashboard & DAX model
├── README.md
└── requirements.txt
```

---

## `〉` Phase 1 — SQL Extraction (MySQL)

The raw dataset exceeds 32 million rows and cannot be loaded into Power BI without prior aggregation. MySQL handled all joins, window functions, and groupings before export.

**Query 1 — Platform KPIs**

```sql
-- Order & customer volume
SELECT
    FORMAT(COUNT(DISTINCT order_id), 0) AS total_orders,
    FORMAT(COUNT(DISTINCT user_id), 0)  AS total_customers
FROM orders;

-- Average basket size
WITH BasketSizes AS (
    SELECT order_id, COUNT(product_id) AS total_items
    FROM order_products
    GROUP BY order_id
)
SELECT ROUND(AVG(total_items), 2) AS avg_basket_size
FROM BasketSizes;

-- Global reorder rate
SELECT
    CONCAT(ROUND((SUM(reordered) / COUNT(*)) * 100, 2), '%') AS global_reorder_rate
FROM order_products;

-- Average days between orders
SELECT
    ROUND(AVG(days_since_prior_order), 2) AS avg_days_between_orders
FROM orders
WHERE days_since_prior_order IS NOT NULL;
```

**Query 2 — Customer Segmentation with Window Functions**

```sql
WITH UserStats AS (
    SELECT
        user_id,
        MAX(order_number)                      AS lifetime_orders,
        ROUND(AVG(days_since_prior_order), 1)  AS avg_days_between_orders
    FROM orders
    GROUP BY user_id
)
SELECT
    user_id,
    lifetime_orders,
    avg_days_between_orders,
    CASE
        WHEN lifetime_orders >= 40 THEN 'VIP Customer'
        WHEN lifetime_orders >= 15 THEN 'Loyal Customer'
        WHEN lifetime_orders >= 5  THEN 'Regular Customer'
        ELSE                            'Occasional Customer'
    END AS customer_segment,
    RANK() OVER (ORDER BY lifetime_orders DESC) AS company_rank
FROM UserStats
ORDER BY lifetime_orders DESC
LIMIT 50;
```

**Query 3 — Department Reorder Rate**

```sql
SELECT
    d.department,
    FORMAT(COUNT(op.product_id), 0)                            AS total_items_sold,
    CONCAT(ROUND((SUM(op.reordered)
        / COUNT(op.reordered)) * 100, 2), '%')                 AS reorder_rate
FROM order_products op
JOIN products    p ON op.product_id   = p.product_id
JOIN departments d ON p.department_id = d.department_id
GROUP BY d.department
ORDER BY (SUM(op.reordered) / COUNT(op.reordered)) DESC;
```

**Query 4 — Temporal Heatmap Data**

```sql
SELECT
    order_dow          AS day_of_week,
    order_hour_of_day  AS hour_of_day,
    COUNT(order_id)    AS total_orders
FROM orders
GROUP BY order_dow, order_hour_of_day
ORDER BY total_orders DESC;
```

**Query 5 — Market Basket Analysis (Product Affinity)**

A self-join on `order_products` to identify products most frequently purchased within the same transaction. The `<` operator prevents symmetric duplicates — `(A, B)` and `(B, A)` are not counted separately.

```sql
SELECT
    p1.product_name  AS product_A,
    p2.product_name  AS product_B,
    COUNT(*)         AS times_bought_together
FROM order_products op1
JOIN order_products op2
    ON  op1.order_id   = op2.order_id
    AND op1.product_id < op2.product_id
JOIN products p1 ON op1.product_id = p1.product_id
JOIN products p2 ON op2.product_id = p2.product_id
GROUP BY p1.product_name, p2.product_name
ORDER BY times_bought_together DESC
LIMIT 20;
```

---

## `〉` Phase 2 — EDA & Validation (MySQL)

All profiling and validation was performed directly within MySQL across all six core tables to handle the dataset at full scale, without relying on external spreadsheet tooling.

**Null Validation**

Verified that `days_since_prior_order` is null only on a customer's first order — expected behavior, not a data quality issue.

```sql
SELECT COUNT(*) AS first_time_orders
FROM orders
WHERE days_since_prior_order IS NULL;
```

**Outlier Detection**

Identified anomalous basket sizes using `HAVING` to surface orders with 100+ line items.

```sql
SELECT order_id, COUNT(product_id) AS basket_size
FROM order_products
GROUP BY order_id
HAVING basket_size > 100
ORDER BY basket_size DESC;
```

**Referential Integrity Check**

Confirmed zero orphaned records across the star schema before import into Power BI — every `product_id` maps to a valid `department_id` and `aisle_id`.

```sql
SELECT COUNT(*) AS orphaned_products
FROM products p
LEFT JOIN departments d ON p.department_id = d.department_id
LEFT JOIN aisles       a ON p.aisle_id      = a.aisle_id
WHERE d.department_id IS NULL
   OR a.aisle_id      IS NULL;
```

---

## `〉` Phase 3 — Power BI Dashboard

**Data Model — Kimball Star Schema**

| Table | Type | Notes |
|---|---|---|
| `orders` | Fact | Central transaction grain |
| `order_products` | Fact | Line-item level |
| `dim_customers` | Dimension | Derived from UserStats CTE |
| `products` | Dimension | Joined on `product_id` |
| `departments` | Dimension | Joined on `department_id` |
| `aisles` | Dimension | Joined on `aisle_id` |

Filter direction is strictly `1:*` flowing downstream.

**DAX Measures**

```dax
Total Customers     = DISTINCTCOUNT('dim_customers'[user_id])

Avg Basket Size     =
DIVIDE(
    COUNTROWS('order_products'),
    DISTINCTCOUNT('orders'[order_id]),
    0
)

Global Reorder Rate =
DIVIDE(
    CALCULATE(
        COUNTROWS('order_products'),
        'order_products'[reordered] = 1
    ),
    COUNTROWS('order_products'),
    0
)

-- DAX Anchor (resolves directional filter trap — see Engineering Notes)
Total Items Bought  = COUNTROWS('order_products')
```

---

## `〉` Phase 4 — Python Visualizations (Embedded in Power BI)

Standard Power BI chart types do not support statistical distribution shapes. Python was embedded directly into the canvas via the Power BI Python visual.

**Visualization 1 — Hourly Demand Ridge Plot**

Plots exact transaction volume by hour of day for each department. `seaborn.kdeplot` was not used as it forces smoothed bell curves over pre-aggregated data; a manual `matplotlib` loop preserves the actual transactional shape.

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

dataset = dataset.dropna()

volume_col = [
    col for col in dataset.columns
    if col not in ['department', 'order_hour_of_day']
][0]

dataset     = dataset.sort_values(by=['department', 'order_hour_of_day'])
departments = dataset['department'].unique()
colors      = sns.color_palette("crest", n_colors=len(departments))

sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 7))

for idx, dept in enumerate(departments):
    dept_data = dataset[dataset['department'] == dept]
    plt.plot(
        dept_data['order_hour_of_day'],
        dept_data[volume_col],
        color=colors[idx], linewidth=3, label=dept
    )
    plt.fill_between(
        dept_data['order_hour_of_day'],
        dept_data[volume_col],
        color=colors[idx], alpha=0.3
    )

plt.title('Hourly Order Volume by Department', fontsize=18, fontweight='bold', pad=20)
plt.xlabel('Hour of Day (0–23)', fontsize=14, fontweight='bold', labelpad=10)
plt.ylabel('Total Orders',       fontsize=14, fontweight='bold', labelpad=10)
plt.xticks(range(0, 24), fontsize=12, fontweight='bold')
plt.xlim(0, 23)
plt.ylim(0, dataset[volume_col].max() * 1.1)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'size': 12, 'weight': 'bold'})
plt.tight_layout()
plt.show()
```

**Visualization 2 — Customer Frequency Violin Plot**

Visualizes the statistical density of average days between orders by customer loyalty tier. A `Top 100k` Visual Level Filter (driven by `Total Items Bought`) was applied to stay within Power BI's Python row limit.

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

dataset = dataset.dropna()

cat_cols = dataset.select_dtypes(include=['object', 'category']).columns
num_cols = dataset.select_dtypes(include=['float64', 'int64']).columns

segment_col = [col for col in cat_cols if 'segment' in col.lower() or 'customer' in col.lower()][0]
days_col    = [col for col in num_cols if 'days'    in col.lower() or 'avg'      in col.lower()][0]

order = ['VIP Customer', 'Loyal Customer', 'Regular Customer', 'Occasional Customer']

sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

sns.violinplot(
    x=days_col, y=segment_col,
    data=dataset, order=order,
    palette="magma", inner="quartile"
)

plt.title('Purchasing Frequency Distribution by Customer Segment',
          fontsize=16, fontweight='bold', pad=15)
plt.xlabel('Average Days Between Orders', fontsize=12, fontweight='bold')
plt.ylabel('', fontsize=12)
plt.tight_layout()
plt.show()
```

---

## `〉` Engineering Notes

**Directional Filter Trap**

Power BI filters flow strictly downstream. Selecting a dimension value (e.g., "Produce") did not propagate to the `dim_customers` Python visual because the filter path terminated at the bottom of the schema.

Resolution: The `Total Items Bought` DAX measure was added to the Python visual's field well. Power BI assigns `BLANK` to customers outside the filtered context and drops blank rows automatically before executing Python — reversing the effective filter direction without schema changes.

**Dynamic Column Aliasing**

Power BI silently renames columns placed into visual wells (e.g., `order_id` becomes `Count of order_id`). Hardcoded references in Python caused `KeyError` failures when naming changed.

Resolution: Python list comprehensions scan `dataset.columns` at runtime using data type and substring matching, decoupling scripts from Power BI's UI naming conventions entirely.

**Dashboard State Reset**

Python renders as a static image inside Power BI; interactive controls cannot be embedded within the visual itself.

Resolution: A native Power BI **Bookmark** was configured as a global reset button, clearing all active slicer states and returning the canvas to its default view.

---

## `〉` Key Findings

| Finding | Detail |
|---|---|
| **Volume concentration** | Produce and Dairy account for a disproportionate share of transaction volume, indicating that product freshness is the primary driver of platform retention |
| **Temporal patterns** | Staple groceries peak Sunday afternoon; Alcohol and Snacks show distinct secondary peaks in late evening hours — relevant for dynamic shift scheduling |
| **VIP cohort behavior** | VIP customers show a narrow, predictable frequency distribution concentrated around the 4–7 day mark, making this segment well-suited for subscription model targeting |

---

## `〉` Local Setup

### 1 · Clone the repository

```bash
git clone https://github.com/YourUsername/qcommerce-analytics.git
cd qcommerce-analytics
```

### 2 · Download the dataset

The raw `.csv` files exceed GitHub's size limit. Download from Kaggle:
[https://www.kaggle.com/c/instacart-market-basket-analysis](https://www.kaggle.com/c/instacart-market-basket-analysis)

Place files in the `/data` directory.

### 3 · Run SQL scripts

Execute in order within your local MySQL environment:

```
sql/00_eda_data_validation.sql
sql/01_core_kpis.sql
sql/02_customer_segmentation.sql
sql/03_department_reorders.sql
sql/04_temporal_logistics.sql
sql/05_market_basket.sql
```

### 4 · Install Python dependencies

```bash
pip install -r requirements.txt
# pandas · matplotlib · seaborn
```

### 5 · Open the dashboard

```
Open powerbi/Instacart_Dashboard.pbix in Power BI Desktop
→ File > Options > Python scripting
→ Map to your local Python environment
→ Refresh all visuals
```

---

## `〉` Potential Extensions

| Extension | Approach |
|---|---|
| **Association Rules** | Apply Apriori or FP-Growth to the market basket data for formal lift and confidence scoring beyond raw co-occurrence counts |
| **Churn Prediction** | Use `days_since_prior_order` distribution to train a logistic regression model identifying customers at risk of lapsing |
| **Cloud Scale** | Migrate MySQL aggregations to BigQuery or Snowflake to process the full 32M row dataset without pre-aggregation |

---

<div align="center">

<br/>

![Footer](https://img.shields.io/badge/Q--Commerce_Analytics-Grocery_Order_Intelligence_Pipeline-217346?style=for-the-badge&labelColor=000000&logoColor=white)

</div>
