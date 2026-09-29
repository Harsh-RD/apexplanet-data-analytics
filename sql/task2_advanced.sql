-- Task 2: Advanced SQL Concepts
-- Dataset: Online Retail

-- 1. Filtering Groups with HAVING
SELECT Country, ROUND(SUM(TotalSales), 2) AS TotalSales
FROM transactions
GROUP BY Country
HAVING SUM(TotalSales) > 100000
ORDER BY TotalSales DESC;

-- 2. Monthly Revenue Extraction (Time-series analysis)
SELECT 
    strftime('%Y-%m', InvoiceDate) AS Month,
    ROUND(SUM(TotalSales), 2) AS MonthlyRevenue
FROM transactions
GROUP BY Month
ORDER BY Month;
