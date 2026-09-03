-- ============================================================
-- API WEATHER DATA PIPELINE
-- ADVANCED SQL ANALYTICS
-- ============================================================


-- ============================================================
-- 1. VIEW ALL WEATHER DATA
-- ============================================================

SELECT
    id,
    timestamp,
    temperature_c,
    humidity_pct,
    wind_speed_kmh,
    city
FROM weather_data
ORDER BY timestamp;


-- ============================================================
-- 2. TOTAL RECORDS
-- ============================================================

SELECT
    COUNT(*) AS total_records
FROM weather_data;


-- ============================================================
-- 3. WEATHER SUMMARY
-- ============================================================

SELECT
    COUNT(*) AS total_records,

    ROUND(AVG(temperature_c), 2)
        AS average_temperature,

    MAX(temperature_c)
        AS maximum_temperature,

    MIN(temperature_c)
        AS minimum_temperature,

    ROUND(AVG(humidity_pct), 2)
        AS average_humidity,

    MAX(humidity_pct)
        AS maximum_humidity,

    MIN(humidity_pct)
        AS minimum_humidity,

    ROUND(AVG(wind_speed_kmh), 2)
        AS average_wind_speed,

    MAX(wind_speed_kmh)
        AS maximum_wind_speed

FROM weather_data;


-- ============================================================
-- 4. TEMPERATURE CLASSIFICATION
-- ============================================================

SELECT
    timestamp,
    temperature_c,

    CASE
        WHEN temperature_c < 20
            THEN 'Cold'

        WHEN temperature_c >= 20
             AND temperature_c < 30
            THEN 'Moderate'

        WHEN temperature_c >= 30
             AND temperature_c < 40
            THEN 'Hot'

        ELSE 'Extreme'
    END AS temperature_category,

    city

FROM weather_data

ORDER BY timestamp;


-- ============================================================
-- 5. TEMPERATURE RANKING
-- ============================================================

SELECT
    timestamp,
    temperature_c,

    RANK() OVER (
        ORDER BY temperature_c DESC
    ) AS temperature_rank,

    city

FROM weather_data

ORDER BY temperature_rank;


-- ============================================================
-- 6. TOP 5 HOTTEST HOURS
-- ============================================================

SELECT
    timestamp,
    temperature_c,
    city

FROM weather_data

ORDER BY temperature_c DESC

LIMIT 5;


-- ============================================================
-- 7. TOP 5 COLDEST HOURS
-- ============================================================

SELECT
    timestamp,
    temperature_c,
    city

FROM weather_data

ORDER BY temperature_c ASC

LIMIT 5;


-- ============================================================
-- 8. HOTTEST PERIOD
-- ============================================================

SELECT
    timestamp,
    temperature_c,
    city

FROM weather_data

ORDER BY temperature_c DESC

LIMIT 1;


-- ============================================================
-- 9. COLDEST PERIOD
-- ============================================================

SELECT
    timestamp,
    temperature_c,
    city

FROM weather_data

ORDER BY temperature_c ASC

LIMIT 1;


-- ============================================================
-- 10. HIGHEST HUMIDITY
-- ============================================================

SELECT
    timestamp,
    humidity_pct,
    city

FROM weather_data

ORDER BY humidity_pct DESC

LIMIT 1;


-- ============================================================
-- 11. LOWEST HUMIDITY
-- ============================================================

SELECT
    timestamp,
    humidity_pct,
    city

FROM weather_data

ORDER BY humidity_pct ASC

LIMIT 1;


-- ============================================================
-- 12. STRONGEST WIND
-- ============================================================

SELECT
    timestamp,
    wind_speed_kmh,
    city

FROM weather_data

ORDER BY wind_speed_kmh DESC

LIMIT 1;


-- ============================================================
-- 13. WEAKEST WIND
-- ============================================================

SELECT
    timestamp,
    wind_speed_kmh,
    city

FROM weather_data

ORDER BY wind_speed_kmh ASC

LIMIT 1;


-- ============================================================
-- 14. 3-HOUR MOVING AVERAGE
-- ============================================================

SELECT
    timestamp,
    temperature_c,

    ROUND(
        AVG(temperature_c) OVER (
            ORDER BY timestamp
            ROWS BETWEEN 2 PRECEDING
            AND CURRENT ROW
        ),
        2
    ) AS moving_average_3h

FROM weather_data

ORDER BY timestamp;


-- ============================================================
-- 15. HOURLY WEATHER ANALYSIS
-- ============================================================

SELECT

    EXTRACT(
        HOUR FROM timestamp
    ) AS hour,

    ROUND(
        AVG(temperature_c),
        2
    ) AS average_temperature,

    ROUND(
        AVG(humidity_pct),
        2
    ) AS average_humidity,

    ROUND(
        AVG(wind_speed_kmh),
        2
    ) AS average_wind_speed

FROM weather_data

GROUP BY
    EXTRACT(HOUR FROM timestamp)

ORDER BY hour;


-- ============================================================
-- 16. DAILY WEATHER SUMMARY
-- ============================================================

SELECT

    DATE(timestamp)
        AS weather_date,

    ROUND(
        AVG(temperature_c),
        2
    ) AS average_temperature,

    MAX(temperature_c)
        AS maximum_temperature,

    MIN(temperature_c)
        AS minimum_temperature,

    ROUND(
        AVG(humidity_pct),
        2
    ) AS average_humidity,

    MAX(humidity_pct)
        AS maximum_humidity,

    ROUND(
        AVG(wind_speed_kmh),
        2
    ) AS average_wind_speed,

    MAX(wind_speed_kmh)
        AS maximum_wind_speed

FROM weather_data

GROUP BY
    DATE(timestamp)

ORDER BY weather_date;


-- ============================================================
-- 17. TEMPERATURE TREND
-- ============================================================

SELECT

    timestamp,

    temperature_c,

    LAG(temperature_c)
        OVER (
            ORDER BY timestamp
        )
        AS previous_temperature,

    ROUND(
        temperature_c
        -
        LAG(temperature_c)
        OVER (
            ORDER BY timestamp
        ),
        2
    )
        AS temperature_change

FROM weather_data

ORDER BY timestamp;


-- ============================================================
-- 18. HIGHEST TEMPERATURE CHANGE
-- ============================================================

WITH temperature_changes AS (

    SELECT

        timestamp,

        temperature_c,

        LAG(temperature_c)
            OVER (
                ORDER BY timestamp
            )
            AS previous_temperature

    FROM weather_data
)

SELECT

    timestamp,

    temperature_c,

    previous_temperature,

    ROUND(
        temperature_c
        - previous_temperature,
        2
    ) AS temperature_change

FROM temperature_changes

WHERE previous_temperature IS NOT NULL

ORDER BY ABS(
    temperature_c
    - previous_temperature
) DESC

LIMIT 1;


-- ============================================================
-- 19. WEATHER CONDITIONS BY HOUR
-- ============================================================

SELECT

    timestamp,

    temperature_c,

    humidity_pct,

    wind_speed_kmh,

    CASE

        WHEN temperature_c >= 35
             AND humidity_pct >= 70
            THEN 'Very Hot & Humid'

        WHEN temperature_c >= 35
            THEN 'Very Hot'

        WHEN temperature_c >= 30
             AND humidity_pct >= 70
            THEN 'Hot & Humid'

        WHEN temperature_c >= 30
            THEN 'Hot'

        WHEN temperature_c < 20
            THEN 'Cold'

        ELSE 'Moderate'

    END AS weather_condition,

    city

FROM weather_data

ORDER BY timestamp;


-- ============================================================
-- 20. CITY SUMMARY
-- ============================================================

SELECT

    city,

    COUNT(*) AS total_records,

    ROUND(
        AVG(temperature_c),
        2
    ) AS average_temperature,

    MAX(temperature_c)
        AS maximum_temperature,

    MIN(temperature_c)
        AS minimum_temperature,

    ROUND(
        AVG(humidity_pct),
        2
    ) AS average_humidity,

    ROUND(
        AVG(wind_speed_kmh),
        2
    ) AS average_wind_speed

FROM weather_data

GROUP BY city

ORDER BY city;


-- ============================================================
-- 21. DATA QUALITY SUMMARY
-- ============================================================

SELECT

    COUNT(*) AS total_records,

    COUNT(*) FILTER (
        WHERE temperature_c IS NULL
    ) AS null_temperature,

    COUNT(*) FILTER (
        WHERE humidity_pct IS NULL
    ) AS null_humidity,

    COUNT(*) FILTER (
        WHERE wind_speed_kmh IS NULL
    ) AS null_wind_speed,

    COUNT(*) FILTER (
        WHERE timestamp IS NULL
    ) AS null_timestamp,

    COUNT(*) FILTER (
        WHERE temperature_c < -90
           OR temperature_c > 60
    ) AS invalid_temperature,

    COUNT(*) FILTER (
        WHERE humidity_pct < 0
           OR humidity_pct > 100
    ) AS invalid_humidity,

    COUNT(*) FILTER (
        WHERE wind_speed_kmh < 0
    ) AS invalid_wind_speed

FROM weather_data;


-- ============================================================
-- 22. DASHBOARD KPI QUERY
-- ============================================================

SELECT

    ROUND(
        AVG(temperature_c),
        2
    ) AS average_temperature,

    MAX(temperature_c)
        AS maximum_temperature,

    MIN(temperature_c)
        AS minimum_temperature,

    ROUND(
        AVG(humidity_pct),
        2
    ) AS average_humidity,

    ROUND(
        AVG(wind_speed_kmh),
        2
    ) AS average_wind_speed,

    MAX(wind_speed_kmh)
        AS maximum_wind_speed,

    COUNT(*) AS total_records

FROM weather_data;


-- ============================================================
-- 23. DASHBOARD HOURLY CHART DATA
-- ============================================================

SELECT

    timestamp,

    temperature_c,

    humidity_pct,

    wind_speed_kmh

FROM weather_data

ORDER BY timestamp;


-- ============================================================
-- 24. RECENT WEATHER DATA
-- ============================================================

SELECT

    timestamp,

    temperature_c,

    humidity_pct,

    wind_speed_kmh,

    city

FROM weather_data

ORDER BY timestamp DESC

LIMIT 10;
CREATE OR REPLACE VIEW weather_daily_summary AS

SELECT

    DATE(timestamp) AS weather_date,

    city,

    COUNT(*) AS total_records,

    ROUND(
        AVG(temperature_c),
        2
    ) AS average_temperature,

    MAX(temperature_c)
        AS maximum_temperature,

    MIN(temperature_c)
        AS minimum_temperature,

    ROUND(
        AVG(humidity_pct),
        2
    ) AS average_humidity,

    MAX(humidity_pct)
        AS maximum_humidity,

    ROUND(
        AVG(wind_speed_kmh),
        2
    ) AS average_wind_speed,

    MAX(wind_speed_kmh)
        AS maximum_wind_speed

FROM weather_data

GROUP BY
    DATE(timestamp),
    city

ORDER BY weather_date;
SELECT *
FROM weather_daily_summary;