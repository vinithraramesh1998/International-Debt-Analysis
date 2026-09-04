USE international_debt_db;


-- =========================================================
-- Q1. Retrieve all distinct country names from the dataset
-- =========================================================

SELECT DISTINCT country_name
FROM countries;


-- =========================================================
-- Q2. Count the total number of countries available
-- =========================================================

SELECT COUNT(*) AS total_countries
FROM countries;


-- =========================================================
-- Q3. Find the total number of indicators present
-- =========================================================

SELECT COUNT(*) AS total_indicators
FROM indicators;


-- =========================================================
-- Q4. Display the first 10 records of the dataset
-- =========================================================

SELECT *
FROM debt_data
LIMIT 10;


-- =========================================================
-- Q5. Calculate the total global debt
-- =========================================================

SELECT SUM(debt_value) AS total_global_debt
FROM debt_data;


-- =========================================================
-- Q6. List all unique indicator names
-- =========================================================

SELECT DISTINCT series_name
FROM indicators;


-- =========================================================
-- Q7. Find the number of records for each country
-- =========================================================

SELECT 
    country_code,
    COUNT(*) AS total_records
FROM debt_data
GROUP BY country_code
ORDER BY total_records DESC;


-- =========================================================
-- Q8. Display all records where debt is greater than 1 billion USD
-- =========================================================

SELECT *
FROM debt_data
WHERE debt_value > 1000000000;


-- =========================================================
-- Q9. Find the minimum, maximum, and average debt values
-- =========================================================

SELECT
    MIN(debt_value) AS minimum_debt,
    MAX(debt_value) AS maximum_debt,
    AVG(debt_value) AS average_debt
FROM debt_data;


-- =========================================================
-- Q10. Count the total number of records in the dataset
-- =========================================================

SELECT COUNT(*) AS total_records
FROM debt_data;


-- =========================================================
-- Q11. Find the total debt for each country
-- =========================================================

SELECT
    country_code,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_code
ORDER BY total_debt DESC;


-- =========================================================
-- Q12. Display the top 10 countries with the highest total debt
-- =========================================================

SELECT
    country_code,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_code
ORDER BY total_debt DESC
LIMIT 10;


-- =========================================================
-- Q13. Find the average debt per country
-- =========================================================

SELECT
    country_code,
    AVG(debt_value) AS average_debt
FROM debt_data
GROUP BY country_code
ORDER BY average_debt DESC;


-- =========================================================
-- Q14. Calculate total debt for each indicator
-- =========================================================

SELECT
    series_code,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY series_code
ORDER BY total_debt DESC;


-- =========================================================
-- Q15. Identify the indicator contributing the highest total debt
-- =========================================================

SELECT
    series_code,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY series_code
ORDER BY total_debt DESC
LIMIT 1;


-- =========================================================
-- Q16. Find the country with the lowest total debt
-- =========================================================

SELECT
    country_code,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_code
ORDER BY total_debt ASC
LIMIT 1;


-- =========================================================
-- Q17. Calculate total debt for each country and indicator
-- Python Query Q7 converted to SQL
-- =========================================================

SELECT
    country_code,
    series_code,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_code, series_code
ORDER BY total_debt DESC;


-- =========================================================
-- Q18. Count how many indicators each country has
-- Python Query Q8 converted to SQL
-- =========================================================

SELECT
    country_code,
    COUNT(DISTINCT series_code) AS indicator_count
FROM debt_data
GROUP BY country_code
ORDER BY indicator_count DESC;


-- =========================================================
-- Q19. Calculate total debt for each country and year
-- Python Query Q9 converted to SQL
-- =========================================================

SELECT
    country_code,
    year,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_code, year
ORDER BY total_debt DESC;


-- =========================================================
-- Q20. Calculate the average debt for each country
-- Python Query Q10 converted to SQL
-- =========================================================

SELECT
    country_code,
    AVG(debt_value) AS average_debt
FROM debt_data
GROUP BY country_code
ORDER BY average_debt DESC;


-- =========================================================
-- Q21. Display country and indicator-wise total debt
-- =========================================================

SELECT
    country_code,
    series_code,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_code, series_code
ORDER BY total_debt DESC;


-- =========================================================
-- Q22. Display 10 country and indicator combinations
-- =========================================================

SELECT
    country_code,
    series_code,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_code, series_code
LIMIT 10;


-- =========================================================
-- Q23. Check whether the SQL query is working
-- =========================================================

SELECT 1;


-- =========================================================
-- Q24. Find indicator-wise total debt for China
-- =========================================================

SELECT
    country_code,
    series_code,
    SUM(debt_value) AS total_debt
FROM debt_data
WHERE country_code = 'CHN'
GROUP BY country_code, series_code;


-- =========================================================
-- Q25. Count the total number of debt records for China
-- =========================================================

SELECT COUNT(*) AS total_records
FROM debt_data
WHERE country_code = 'CHN';


-- =========================================================
-- Q26. Display 10 country and indicator combinations with total debt
-- =========================================================

SELECT
    country_code,
    series_code,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_code, series_code
LIMIT 10;


-- =========================================================
-- Q27. Show the indexes available on the debt_data table
-- =========================================================

SHOW INDEX FROM debt_data;


-- =========================================================
-- Q28. Explain the execution plan for the country-indicator query
-- =========================================================

EXPLAIN
SELECT
    country_code,
    series_code,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY country_code, series_code
LIMIT 10;


-- =========================================================
-- Q29. Count the number of indicators available for each country
-- =========================================================

SELECT
    country_code,
    COUNT(DISTINCT series_code) AS indicator_count
FROM debt_data
GROUP BY country_code
ORDER BY indicator_count DESC;


-- =========================================================
-- Q30. Find the top 5 indicators contributing most to total debt
-- =========================================================

SELECT 
    series_code,
    SUM(debt_value) AS total_debt
FROM debt_data
GROUP BY series_code
ORDER BY total_debt DESC
LIMIT 5;

