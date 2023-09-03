-- AVERAGE PLAYERS PER SESSION
WITH PERSONS_PER_SESSION AS(
SELECT M."DATE", COUNT(DISTINCT M."PLAYER_ID") AS PERSONS_PER_SESSION
FROM stats_bg.bronze."MATCHES" M
GROUP BY 1
)
SELECT CEILING(AVG(PERSONS_PER_SESSION) - 0.5) AS "AVG_PERSONS_PER_SESSION"
FROM PERSONS_PER_SESSION
WHERE  extract(year from to_date("DATE", '%dd%mm%YY')) = extract(year from CURRENT_DATE)