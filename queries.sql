-- 1. Top 10 vehicles involved in drug-related stops
SELECT * FROM traffic_stops
WHERE drugs_related_stop = TRUE
LIMIT 10;

-- 2. Vehicles most frequently searched
SELECT violation, COUNT(*) AS search_count
FROM traffic_stops
WHERE search_conducted = TRUE
GROUP BY violation
ORDER BY search_count DESC
LIMIT 10;

-- 3. Driver age group with the highest arrest rate
SELECT driver_age, COUNT(*) AS arrest_count
FROM traffic_stops
WHERE is_arrested = TRUE
GROUP BY driver_age
ORDER BY arrest_count DESC
LIMIT 1;

-- 4. Gender distribution of drivers stopped in each country
SELECT country_name, driver_gender, COUNT(*) AS total_stops
FROM traffic_stops
GROUP BY country_name, driver_gender
ORDER BY country_name;

-- 5. Race and gender combination with highest search rate
SELECT driver_race, driver_gender, COUNT(*) AS search_count
FROM traffic_stops
WHERE search_conducted = TRUE
GROUP BY driver_race, driver_gender
ORDER BY search_count DESC
LIMIT 1;

-- 6. What time of day sees the most traffic stops
SELECT HOUR(stop_time) AS hour_of_day, COUNT(*) AS total_stops
FROM traffic_stops
GROUP BY hour_of_day
ORDER BY total_stops DESC
LIMIT 1;

-- 7. Average stop duration for different violations
SELECT violation, AVG(
    CASE stop_duration
        WHEN '<5 Min' THEN 3
        WHEN '6-15 Min' THEN 10
        WHEN '16-30 Min' THEN 20
        WHEN '30+ Min' THEN 35
    END
) AS avg_duration_minutes
FROM traffic_stops
GROUP BY violation;

-- 8. Are night stops more likely to lead to arrests?
SELECT
    CASE
        WHEN HOUR(stop_time) BETWEEN 20 AND 23 THEN 'Night'
        WHEN HOUR(stop_time) BETWEEN 0 AND 5 THEN 'Late Night'
        ELSE 'Day'
    END AS time_period,
    COUNT(*) AS total_stops,
    SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests
FROM traffic_stops
GROUP BY time_period;

-- 9. Violations most associated with searches or arrests
SELECT violation,
       COUNT(*) AS total_stops,
       SUM(search_conducted) AS search_count,
       SUM(is_arrested) AS arrest_count
FROM traffic_stops
GROUP BY violation
ORDER BY search_count DESC, arrest_count DESC
LIMIT 5;

-- 10. Violations most common among drivers <25
SELECT violation, COUNT(*) AS young_driver_count
FROM traffic_stops
WHERE driver_age < 25
GROUP BY violation
ORDER BY young_driver_count DESC;

-- 11. Violation that rarely results in search or arrest
SELECT violation,
       COUNT(*) AS total,
       SUM(search_conducted) AS searches,
       SUM(is_arrested) AS arrests
FROM traffic_stops
GROUP BY violation
ORDER BY searches ASC, arrests ASC
LIMIT 3;

-- 12. Countries with highest rate of drug-related stops
SELECT country_name, COUNT(*) AS total_drug_stops
FROM traffic_stops
WHERE drugs_related_stop = TRUE
GROUP BY country_name
ORDER BY total_drug_stops DESC;

-- 13. Arrest rate by country and violation
SELECT country_name, violation,
       COUNT(*) AS total_stops,
       SUM(is_arrested) AS total_arrests,
       ROUND(SUM(is_arrested)/COUNT(*) * 100, 2) AS arrest_rate_percent
FROM traffic_stops
GROUP BY country_name, violation
ORDER BY arrest_rate_percent DESC;

-- 14. Country with most stops where search was conducted
SELECT country_name, COUNT(*) AS search_count
FROM traffic_stops
WHERE search_conducted = TRUE
GROUP BY country_name
ORDER BY search_count DESC
LIMIT 1;

-- 15. Yearly breakdown of stops and arrests by country
SELECT country_name, 
       YEAR(stop_date) AS year,
       COUNT(*) AS total_stops,
       SUM(is_arrested) AS total_arrests
FROM traffic_stops
GROUP BY country_name, YEAR(stop_date)
ORDER BY country_name, year;

-- 16. Driver violation trends by age and race
SELECT driver_age, driver_race, violation, COUNT(*) AS violation_count
FROM traffic_stops
GROUP BY driver_age, driver_race, violation
ORDER BY driver_age;

-- 17. Number of stops by year, month, and hour
SELECT
    YEAR(stop_date) AS year,
    MONTH(stop_date) AS month,
    HOUR(stop_time) AS hour,
    COUNT(*) AS total_stops
FROM traffic_stops
GROUP BY YEAR(stop_date), MONTH(stop_date), HOUR(stop_time)
ORDER BY year, month, hour;

-- 18. Violations with highest search and arrest rates
SELECT violation,
       COUNT(*) AS total,
       SUM(search_conducted) AS search_count,
       SUM(is_arrested) AS arrest_count,
       ROUND(SUM(search_conducted)/COUNT(*) * 100, 2) AS search_rate,
       ROUND(SUM(is_arrested)/COUNT(*) * 100, 2) AS arrest_rate
FROM traffic_stops
GROUP BY violation
ORDER BY arrest_rate DESC
LIMIT 5;

-- 19. Driver demographics by country
SELECT country_name, driver_gender, driver_race, AVG(driver_age) AS avg_age, COUNT(*) AS total_drivers
FROM traffic_stops
GROUP BY country_name, driver_gender, driver_race;

-- 20. Top 5 violations with highest arrest rate
SELECT violation,
       COUNT(*) AS total_violations,
       SUM(is_arrested) AS total_arrests,
       ROUND(SUM(is_arrested)/COUNT(*) * 100, 2) AS arrest_rate
FROM traffic_stops
GROUP BY violation
ORDER BY arrest_rate DESC
LIMIT 5;
