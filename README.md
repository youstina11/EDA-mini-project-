# EDA Mini Project — Enhanced (Employee + Superstore)

Building an End-to-End Data Pipeline: Python EDA & SQLite Integration.

This is an **enhanced version** of the original Employee EDA/SQLite mini-project.
It keeps the original employee pipeline intact and adds a second, larger
real-world pipeline built on the **Sample Superstore 2019** retail dataset
(Orders, People, Returns), plus auto-generated chart images and a pipeline
architecture diagram.

## What's new in this version

- **New dataset module**: `scripts/02_superstore_solution.py` — a full EDA →
  cleaning → feature engineering → SQLite → SQL analytics → aggregation →
  visualization → export pipeline for the Superstore Orders/People/Returns data.
- **8 generated charts** (`outputs/charts/`): sales by category, profit by
  region, monthly sales trend, profit by sub-category, discount vs. profit
  margin, sales-vs-profit scatter, a correlation heatmap, and a segment mix
  pie chart.
- **A visual pipeline diagram** (`outputs/charts/00_pipeline_diagram.png`)
  showing the 9-stage architecture the project follows end to end.
- **Reorganized project layout** (`data/`, `scripts/`, `db/`, `outputs/`) and
  a single `run_pipeline.py` entry point that runs both modules plus the
  diagram generator in one command.
- **Original employee module preserved** as `scripts/01_employee_solution.py`
  (paths updated to fit the new folder layout; logic unchanged).

## Project structure

```
EDA-mini-project-Enhanced/
├── data/
│   ├── EDA_SQLite_Employee_200.csv     # original employee dataset
│   └── Sample_Superstore_2019.xls      # new: Orders / People / Returns sheets
├── scripts/
│   ├── 01_employee_solution.py         # original employee EDA + SQLite pipeline
│   ├── 02_superstore_solution.py       # NEW: superstore EDA + SQLite + charts
│   └── 03_generate_pipeline_diagram.py # NEW: renders the architecture diagram
├── db/
│   ├── employee.db                     # SQLite output (employee pipeline)
│   ├── employee_bonus.db               # SQLite output (bonus functions demo)
│   └── superstore.db                   # SQLite output (superstore pipeline)
├── outputs/
│   ├── charts/                         # all generated PNG charts (9 files)
│   └── exports/                        # cleaned CSV exports
├── run_pipeline.py                     # runs everything end-to-end
├── README.md
└── EDA_SQLite_Assignment_Solution.pdf  # original assignment write-up
```

## How to run

```bash
pip install pandas numpy matplotlib seaborn xlrd
python run_pipeline.py
```

This runs, in order:
1. `01_employee_solution.py` — cleans the employee dataset, loads it into
   `db/employee.db`, runs CRUD/analytical SQL, exports `employees_final.csv`.
2. `02_superstore_solution.py` — cleans and merges the Superstore
   Orders/People/Returns sheets, engineers features (profit margin, shipping
   lead time, discount bands, return flags, etc.), loads everything into
   `db/superstore.db`, runs analytical + CRUD SQL, aggregates by
   category/region/segment/sub-category/customer, and saves 8 charts.
3. `03_generate_pipeline_diagram.py` — renders the 9-stage pipeline diagram.

## Pipeline architecture

![Pipeline Diagram](outputs/charts/00_pipeline_diagram.png)

`Ingest → EDA → Clean → Feature Engineer → Load SQLite → SQL Analytics → Aggregate → Visualize → Export`

## Superstore module — key techniques demonstrated

- **EDA**: `shape`, `dtypes`, `describe()`, missing-value profiling across
  three linked sheets.
- **Cleaning**: type casting (dates, nullable ints), deduplication, merging
  `Returns` and `People` sheets onto `Orders` to build a single wide table.
- **Feature engineering**: `Profit_Margin`, `Unit_Price`,
  `Shipping_Lead_Days`, calendar parts (year/month/weekday),
  `Is_Profitable`, `Discount_Band` (binned), `High_Value_Order` (90th
  percentile flag), `Is_Returned`.
- **SQLite3**: schema creation, `to_sql()` loads for all three tables,
  parameterized analytical queries, `UPDATE`, `DELETE`, and `INSERT`
  operations, then export back to CSV.
- **Aggregation**: sales/profit by category, region, segment, sub-category;
  monthly sales trend; top customers; return rate by category.
- **Visualization**: bar, line, horizontal bar, box plot, scatter, heatmap,
  and pie charts — each saved as a standalone PNG for reporting/dashboards.

## Original employee module (unchanged logic)

Covers summary statistics, missing-value imputation, duplicate removal,
feature engineering (bonus, total compensation, seniority flag), filtering,
sorting, groupby aggregation, a full SQLite3 CRUD workflow, and reusable
`load_data()` / `clean_data()` / `save_to_sqlite()` functions with
try/except error handling.

## Tech stack

- **Language**: Python
- **Data manipulation**: pandas, NumPy
- **Database**: SQLite3, SQL
- **Visualization**: matplotlib, seaborn
- **Excel I/O**: xlrd (for legacy `.xls` files)
