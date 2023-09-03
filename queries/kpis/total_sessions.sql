-- TOTAL SESSIONS 
SELECT COUNT(DISTINCT M."DATE") AS TOTAL_SESSIONS 
FROM stats_bg.bronze."MATCHES" M 
WHERE  extract(year from to_date("DATE", '%dd%mm%YY')) = extract(year from CURRENT_DATE)