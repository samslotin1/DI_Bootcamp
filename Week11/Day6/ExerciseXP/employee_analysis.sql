SELECT *
FROM df_employee
LIMIT 10;

UPDATE df_employee
SET
    id = TRIM(id),
    employee_id = TRIM(employee_id),
    employee_name = TRIM(employee_name),
    gender = TRIM(gender),
    salary = TRIM(salary),
    function_group = TRIM(function_group),
    company_name = TRIM(company_name),
    company_city = TRIM(company_city),
    company_state = TRIM(company_state),
    company_type = TRIM(company_type),
    const_site_category = TRIM(const_site_category);

SELECT *
FROM df_employee
WHERE id IS NULL
   OR month_year IS NULL
   OR employee_id IS NULL
   OR employee_name IS NULL
   OR gender IS NULL
   OR age IS NULL
   OR salary IS NULL
   OR function_group IS NULL
   OR company_name IS NULL
   OR company_city IS NULL
   OR company_state IS NULL
   OR company_type IS NULL
   OR const_site_category IS NULL
   OR TRIM(id) = ''
   OR TRIM(employee_id) = ''
   OR TRIM(employee_name) = ''
   OR TRIM(gender) = ''
   OR TRIM(salary) = ''
   OR TRIM(function_group) = ''
   OR TRIM(company_name) = ''
   OR TRIM(company_city) = ''
   OR TRIM(company_state) = ''
   OR TRIM(company_type) = ''
   OR TRIM(const_site_category) = '';

DELETE FROM df_employee
WHERE id IS NULL
   OR month_year IS NULL
   OR employee_id IS NULL
   OR employee_name IS NULL
   OR gender IS NULL
   OR age IS NULL
   OR salary IS NULL
   OR function_group IS NULL
   OR company_name IS NULL
   OR company_city IS NULL
   OR company_state IS NULL
   OR company_type IS NULL
   OR const_site_category IS NULL
   OR TRIM(id) = ''
   OR TRIM(employee_id) = ''
   OR TRIM(employee_name) = ''
   OR TRIM(gender) = ''
   OR TRIM(salary) = ''
   OR TRIM(function_group) = ''
   OR TRIM(company_name) = ''
   OR TRIM(company_city) = ''
   OR TRIM(company_state) = ''
   OR TRIM(company_type) = ''
   OR TRIM(const_site_category) = '';

ALTER TABLE df_employee
ALTER COLUMN salary TYPE NUMERIC
USING REPLACE(salary, ',', '.')::NUMERIC;

SELECT COUNT(DISTINCT employee_id) AS employee_count
FROM df_employee
WHERE month_year = (
    SELECT MAX(month_year)
    FROM df_employee
);

SELECT
    company_name,
    COUNT(DISTINCT employee_id) AS employee_count
FROM df_employee
WHERE month_year = (
    SELECT MAX(month_year)
    FROM df_employee
)
GROUP BY company_name
ORDER BY employee_count DESC;

SELECT
    company_city,
    COUNT(DISTINCT employee_id) AS employee_count,
    ROUND(
        COUNT(DISTINCT employee_id) * 100.0
        / SUM(COUNT(DISTINCT employee_id)) OVER (),
        2
    ) AS percentage
FROM df_employee
WHERE month_year = (
    SELECT MAX(month_year)
    FROM df_employee
)
GROUP BY company_city
ORDER BY employee_count DESC;

SELECT
    month_year,
    COUNT(DISTINCT employee_id) AS employee_count
FROM df_employee
GROUP BY month_year
ORDER BY month_year;

WITH monthly_counts AS (
    SELECT
        month_year,
        COUNT(DISTINCT employee_id) AS employee_count
    FROM df_employee
    GROUP BY month_year
)
SELECT
    ROUND(AVG(employee_count), 2) AS avg_employees_per_month
FROM monthly_counts;

SELECT
    month_year,
    COUNT(DISTINCT employee_id) AS employee_count
FROM df_employee
GROUP BY month_year
ORDER BY employee_count ASC
LIMIT 1;

SELECT
    month_year,
    COUNT(DISTINCT employee_id) AS employee_count
FROM df_employee
GROUP BY month_year
ORDER BY employee_count DESC
LIMIT 1;

WITH monthly_function_counts AS (
    SELECT
        month_year,
        function_group,
        COUNT(DISTINCT employee_id) AS employee_count
    FROM df_employee
    GROUP BY month_year, function_group
)
SELECT
    function_group,
    ROUND(AVG(employee_count), 2) AS avg_employees_per_month
FROM monthly_function_counts
GROUP BY function_group
ORDER BY avg_employees_per_month DESC;

SELECT
    EXTRACT(YEAR FROM month_year) AS year,
    ROUND(AVG(salary), 2) AS average_salary
FROM df_employee
GROUP BY EXTRACT(YEAR FROM month_year)
ORDER BY year;
