import pandas as pd
import numpy as np
import logging
import os
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Constants
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / 'data' / 'raw' / 'Online Retail.xlsx'
PROCESSED_DATA_PATH = PROJECT_ROOT / 'data' / 'processed' / 'online_retail_clean.csv'
KPI_REPORT_PATH = PROJECT_ROOT / 'outputs' / 'kpi_report.xlsx'

def load_data(filepath):
    logging.info("Loading raw data...")
    if not filepath.exists():
        logging.error(f"Raw dataset not found at {filepath}")
        logging.error("Please ensure 'Online Retail.xlsx' is placed in 'data/raw/' directory.")
        sys.exit(1)
    
    try:
        df = pd.read_excel(filepath)
        logging.info(f"Successfully loaded raw data with {len(df)} rows.")
        return df
    except Exception as e:
        logging.error(f"Failed to load raw data: {e}")
        sys.exit(1)

def clean_data(df):
    logging.info("Cleaning data...")
    initial_rows = len(df)
    
    # Remove duplicate rows
    df = df.drop_duplicates()
    
    # Convert InvoiceNo to string
    df['InvoiceNo'] = df['InvoiceNo'].astype(str)
    
    # Identify cancelled invoices (usually starts with 'C')
    # Remove cancelled invoices from the main sales-analysis dataset
    df = df[~df['InvoiceNo'].str.startswith('C', na=False)]
    
    # Remove rows where Quantity <= 0
    df = df[df['Quantity'] > 0]
    
    # Remove rows where UnitPrice <= 0
    df = df[df['UnitPrice'] > 0]
    
    # Remove rows with missing CustomerID
    df = df.dropna(subset=['CustomerID'])
    
    # Convert InvoiceDate to datetime
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    # Convert CustomerID to integer
    df['CustomerID'] = df['CustomerID'].astype(int)
    
    final_rows = len(df)
    logging.info(f"Data cleaning complete. Removed {initial_rows - final_rows} rows.")
    return df

def create_features(df):
    logging.info("Creating features...")
    # Create TotalSales
    df['TotalSales'] = df['Quantity'] * df['UnitPrice']
    
    # Create time-based features
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    df['Day'] = df['InvoiceDate'].dt.day
    df['Week'] = df['InvoiceDate'].dt.isocalendar().week
    
    # Format Month to include Year for monthly KPI grouping (e.g., 2010-12)
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    
    return df

def save_processed_data(df, filepath):
    logging.info("Saving processed data...")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    try:
        df.to_csv(filepath, index=False)
        logging.info(f"Processed data saved successfully to {filepath}")
    except Exception as e:
        logging.error(f"Failed to save processed data: {e}")
        sys.exit(1)

def calculate_kpis(df):
    logging.info("Calculating KPIs...")
    kpis = {}
    
    # Overall KPIs
    kpis['Total Revenue'] = df['TotalSales'].sum()
    kpis['Total Orders'] = df['InvoiceNo'].nunique()
    kpis['Total Units Sold'] = df['Quantity'].sum()
    kpis['Unique Customers'] = df['CustomerID'].nunique()
    kpis['Unique Products'] = df['StockCode'].nunique()
    kpis['Average Order Value'] = kpis['Total Revenue'] / kpis['Total Orders'] if kpis['Total Orders'] > 0 else 0
    kpis['Average Units per Order'] = kpis['Total Units Sold'] / kpis['Total Orders'] if kpis['Total Orders'] > 0 else 0
    
    # Summary DataFrame
    summary_df = pd.DataFrame([{
        'Metric': k, 'Value': v
    } for k, v in kpis.items()])
    
    # Monthly Sales and Orders
    monthly_sales = df.groupby('YearMonth').agg(
        Total_Revenue=('TotalSales', 'sum'),
        Total_Orders=('InvoiceNo', 'nunique')
    ).reset_index()
    
    # Top 5 products by revenue and quantity
    product_stats = df.groupby(['StockCode', 'Description']).agg(
        Total_Revenue=('TotalSales', 'sum'),
        Total_Quantity=('Quantity', 'sum')
    ).reset_index()
    
    top_products_revenue = product_stats.nlargest(5, 'Total_Revenue')
    top_products_quantity = product_stats.nlargest(5, 'Total_Quantity')
    
    # Country Analysis
    country_stats = df.groupby('Country').agg(
        Total_Revenue=('TotalSales', 'sum'),
        Total_Orders=('InvoiceNo', 'nunique')
    ).reset_index()
    
    top_countries_revenue = country_stats.nlargest(5, 'Total_Revenue')
    
    return {
        'Summary': summary_df,
        'Monthly Sales': monthly_sales,
        'Top Products Revenue': top_products_revenue,
        'Top Products Quantity': top_products_quantity,
        'Country Analysis': country_stats,
        'Top Countries': top_countries_revenue
    }

def export_excel_report(kpi_data, filepath):
    logging.info("Exporting Excel report...")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            # Summary
            kpi_data['Summary'].to_excel(writer, sheet_name='Summary', index=False)
            
            # Monthly Sales
            kpi_data['Monthly Sales'].to_excel(writer, sheet_name='Monthly Sales', index=False)
            
            # Top Products
            start_row = 0
            kpi_data['Top Products Revenue'].to_excel(writer, sheet_name='Top Products', startrow=start_row, index=False)
            
            start_row += len(kpi_data['Top Products Revenue']) + 3
            worksheet = writer.sheets['Top Products']
            worksheet.cell(row=start_row, column=1, value="Top 5 Products by Quantity")
            
            kpi_data['Top Products Quantity'].to_excel(writer, sheet_name='Top Products', startrow=start_row, index=False)
            
            # Country Analysis
            kpi_data['Country Analysis'].to_excel(writer, sheet_name='Country Analysis', index=False)
            
        logging.info(f"Excel report exported successfully to {filepath}")
    except Exception as e:
        logging.error(f"Failed to export Excel report: {e}")
        sys.exit(1)

def main():
    logging.info("Starting automation pipeline...")
    
    # Load Data
    df = load_data(RAW_DATA_PATH)
    
    # Clean Data
    df_clean = clean_data(df)
    
    # Feature Engineering
    df_features = create_features(df_clean)
    
    # Save Processed CSV
    save_processed_data(df_features, PROCESSED_DATA_PATH)
    
    # Calculate KPIs
    kpi_data = calculate_kpis(df_features)
    
    # Export KPI Excel
    export_excel_report(kpi_data, KPI_REPORT_PATH)
    
    logging.info("Pipeline completed successfully.")

if __name__ == "__main__":
    main()
