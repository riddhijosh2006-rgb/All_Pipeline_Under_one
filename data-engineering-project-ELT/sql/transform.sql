-- Transforms raw_customers (staging, untouched CSV data) into the clean,
-- analytics-ready "customers" table. This IS the transform step of ELT -
-- it runs INSIDE Postgres instead of in pandas.
--
-- Safe to re-run: drops and rebuilds "customers" every time.

DROP TABLE IF EXISTS customers;

CREATE TABLE customers AS
WITH deduped AS (
    -- keep only the most recently loaded row per customer_id
    SELECT DISTINCT ON (customer_id::int)
        customer_id::int AS customer_id,
        name,
        age,
        city,
        purchase_amount
    FROM raw_customers
    ORDER BY customer_id::int, _loaded_at DESC
),
age_stats AS (
    -- median age, used to fill missing ages (mirrors the old pandas .fillna(median))
    SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY NULLIF(age, '')::numeric) AS median_age
    FROM deduped
)
SELECT
    d.customer_id,
    COALESCE(NULLIF(TRIM(d.name), ''), 'Unknown') AS name,
    COALESCE(NULLIF(d.age, '')::numeric, s.median_age)::int AS age,
    INITCAP(TRIM(COALESCE(NULLIF(d.city, ''), 'Unknown'))) AS city,
    COALESCE(NULLIF(d.purchase_amount, '')::numeric, 0) AS purchase_amount,
    CASE
        WHEN COALESCE(NULLIF(d.purchase_amount, '')::numeric, 0) >= 5000 THEN 'High'
        ELSE 'Low'
    END AS purchase_category
FROM deduped d
CROSS JOIN age_stats s;

ALTER TABLE customers ADD PRIMARY KEY (customer_id);
