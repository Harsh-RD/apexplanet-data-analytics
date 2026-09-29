-- Task 2: Business Questions
-- Dataset: Online Retail

-- 1. What are the top 5 best-selling products by quantity?
SELECT StockCode, Description, SUM(Quantity) AS TotalQuantity
FROM transactions
GROUP BY StockCode, Description
ORDER BY TotalQuantity DESC
LIMIT 5;

-- 2. What are the top 5 best-selling products by revenue?
SELECT StockCode, Description, ROUND(SUM(TotalSales), 2) AS TotalRevenue
FROM transactions
GROUP BY StockCode, Description
ORDER BY TotalRevenue DESC
LIMIT 5;

-- 3. Who are the top 10 customers based on Customer Lifetime Value (CLV)?
SELECT CustomerID, COUNT(DISTINCT InvoiceNo) AS TotalOrders, ROUND(SUM(TotalSales), 2) AS TotalSpend
FROM transactions
GROUP BY CustomerID
ORDER BY TotalSpend DESC
LIMIT 10;
