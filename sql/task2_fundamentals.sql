-- Task 2: Fundamentals of SQL Data Extraction
-- Dataset: Online Retail

-- 1. Select basic transaction records
SELECT *
FROM transactions
LIMIT 10;

-- 2. Filter transactions by Country and high Revenue
SELECT InvoiceNo, Description, Quantity, UnitPrice, TotalSales
FROM transactions
WHERE Country = 'United Kingdom'
  AND TotalSales > 100
LIMIT 20;

-- 3. Top 5 transactions by TotalSales
SELECT InvoiceNo, Description, TotalSales
FROM transactions
ORDER BY TotalSales DESC
LIMIT 5;

-- 4. Revenue grouped by Country
SELECT Country, ROUND(SUM(TotalSales), 2) AS TotalSales
FROM transactions
GROUP BY Country
ORDER BY TotalSales DESC;
