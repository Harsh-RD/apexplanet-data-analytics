# ApexPlanet Data Analytics Internship

## Project overview
This repository contains the analysis of retail transaction data from the UCI Online Retail dataset. The project explores data cleaning, statistical analysis, SQL for data extraction, customer segmentation, machine learning, and data visualization. An automated pipeline processes raw data and generates actionable business KPIs.

## Dataset
The dataset is the **Online Retail dataset**, consisting of transnational transactions occurring between 01/12/2010 and 09/12/2011 for a UK-based and registered non-store online retail. 
Main fields:
* `InvoiceNo`: Invoice number
* `StockCode`: Product code
* `Description`: Product name
* `Quantity`: Quantities of each product per transaction
* `InvoiceDate`: Date and time of the transaction
* `UnitPrice`: Unit price
* `CustomerID`: Customer number
* `Country`: Country name

## Tasks completed
* **Task 1 — Data Analysis / EDA**
* **Task 2 — SQL for Data Extraction** (`ApexPlanet_Task_2_SQL.ipynb`)
* **Task 3 — Data Visualization**
* **Task 4 — Statistical Analysis, Clustering & Predictive Modeling** (`ApexPlanet_Task_4_Statistics_Clustering_ML.ipynb`)
* **Task 5 — Automated Data Pipeline** (`src/pipeline.py`)

*(Note: Task 1 and 3 are combined/replaced by existing notebooks per project structure.)*

## Pipeline
The pipeline (`src/pipeline.py`) executes the following flow:
1. **Raw Excel** (`data/raw/Online Retail.xlsx`)
2. **Cleaning** (Deduplication, filtering cancellations, handling missing values)
3. **Feature Engineering** (`TotalSales`, `Year`, `Month`, `Day`, `Week`)
4. **Processed CSV** (Saved to `data/processed/online_retail_clean.csv`)
5. **KPI Calculation** (Revenue, orders, customer counts, top products)
6. **Excel Report** (Exported to `outputs/kpi_report.xlsx`)

## How to run
1. Place the `Online Retail.xlsx` raw dataset into the `data/raw/` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the automation pipeline:
   ```bash
   python src/pipeline.py
   ```

## Outputs
* **Cleaned Data**: `data/processed/online_retail_clean.csv`
* **KPI Report**: `outputs/kpi_report.xlsx`

## Automation
For automation on local environments where the dataset cannot be uploaded to GitHub due to size or restrictions, use **Windows Task Scheduler**:
1. Open Windows Task Scheduler.
2. Create a Basic Task, e.g., "ApexPlanet Daily Pipeline".
3. Set the trigger (e.g., daily).
4. Set Action to "Start a program".
5. Program/script: `python` (or full path to python.exe)
6. Add arguments: `src/pipeline.py`
7. Start in: `C:\path\to\apexplanet-data-analytics\apexplanet-data-analytics`

## Project structure
```text
apexplanet-data-analytics/
├── data/
│   ├── raw/
│   │   └── Online Retail.xlsx
│   └── processed/
│       └── online_retail_clean.csv
├── notebooks/
│   ├── ApexPlanet_Task_2_SQL.ipynb
│   └── ApexPlanet_Task_4_Statistics_Clustering_ML.ipynb
├── src/
│   └── pipeline.py
├── outputs/
│   └── kpi_report.xlsx
├── requirements.txt
├── README.md
└── .gitignore
```
