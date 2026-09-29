import os
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'ApexPlanet Data Analytics Internship', 0, 1, 'C')
        self.set_font('Arial', 'I', 12)
        self.cell(0, 10, 'Final Project Report', 0, 1, 'C')
        self.line(10, 30, 200, 30)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 8, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, text)
        self.ln(6)

def create_report(filepath):
    pdf = PDF()
    pdf.add_page()

    # Section 1: Overview
    pdf.chapter_title('1. Project Overview')
    overview = (
        "This report summarizes the work completed during the ApexPlanet Data Analytics Internship. "
        "The project focused on analyzing the UCI Online Retail dataset, which contains transnational "
        "transactions for a UK-based online retail store. The core objectives included data cleaning, "
        "SQL extraction, statistical analysis, machine learning (clustering and predictive modeling), "
        "and the deployment of an automated data pipeline."
    )
    pdf.chapter_body(overview)

    # Section 2: Data Cleaning & Feature Engineering
    pdf.chapter_title('2. Data Cleaning & Feature Engineering (Task 1 & 5)')
    cleaning = (
        "The raw dataset contained 541,909 records. A rigorous data cleaning process was applied: \n"
        "- Duplicate rows were removed.\n"
        "- Cancelled orders (InvoiceNo starting with 'C') were filtered out.\n"
        "- Erroneous records with zero or negative Quantity and UnitPrice were removed.\n"
        "- Missing CustomerID values were handled by dropping incomplete records.\n"
        "- Feature engineering was applied to create 'TotalSales' (Quantity * UnitPrice) and "
        "time-series features (Year, Month, Day, Week).\n"
        "After cleaning, the final processed dataset contained 392,693 pristine records."
    )
    pdf.chapter_body(cleaning)

    # Section 3: SQL for Data Extraction
    pdf.chapter_title('3. SQL Data Extraction (Task 2)')
    sql_text = (
        "Using SQLite, the dataset was queried to extract foundational and advanced business insights. "
        "Queries were designed to identify top-performing product categories, calculate monthly recurring "
        "revenue, and determine the distribution of customer lifetime value (CLV)."
    )
    pdf.chapter_body(sql_text)

    # Section 4: Machine Learning & Statistics
    pdf.chapter_title('4. Statistical Analysis & Clustering (Task 4)')
    ml_text = (
        "Advanced analytics were applied to uncover hidden patterns within customer behaviors:\n"
        "- K-Means Clustering: Customers were segmented based on their Recency, Frequency, and Monetary (RFM) "
        "scores to identify VIP customers, loyalists, and at-risk demographics.\n"
        "- Statistical Inference: Hypothesis testing was used to evaluate differences in purchasing habits "
        "across various geographical regions.\n"
        "- Predictive Modeling: A Linear Regression model was built to predict future customer spend based on "
        "historical activity, yielding measurable performance via R-squared and RMSE metrics."
    )
    pdf.chapter_body(ml_text)

    # Section 5: Automation Pipeline & KPI Results
    pdf.chapter_title('5. Automation Pipeline & Business Insights (Task 5)')
    pipeline_text = (
        "A robust, end-to-end Python automation pipeline was deployed to process raw data consistently. "
        "The pipeline loads data, executes the cleaning rules, calculates Key Performance Indicators (KPIs), "
        "and exports an automated multi-sheet Excel report.\n\n"
        "Key Business KPIs Derived:\n"
        "- Total Revenue: £ 8,887,209\n"
        "- Total Orders: 18,532\n"
        "- Total Units Sold: 5,152,002\n"
        "- Unique Customers: 4,338\n"
        "- Unique Products: 3,665\n"
        "- Average Order Value (AOV): £ 479.56\n"
        "- Average Units per Order: 278"
    )
    pdf.chapter_body(pipeline_text)

    # Output
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    pdf.output(filepath, 'F')
    print(f"PDF report successfully generated at: {filepath}")

if __name__ == '__main__':
    create_report(r'c:\Users\admin\.antigravity-ide\apexplanet-data-analytics\apexplanet-data-analytics\reports\final_report.pdf')
