-- AVERAGE GAME PER SESSION
WITH GAMES_PER_SESSION AS(
SELECT M."DATE", COUNT(DISTINCT M."GAME_ID") AS GAMES_PER_SESSION
FROM stats_bg.bronze."MATCHES" M
GROUP BY 1
)
SELECT CEILING(AVG(GAMES_PER_SESSION) - 0.5) AS AVG_GAMES_PER_SESSION
FROM GAMES_PER_SESSION
WHERE  extract(year from to_date("DATE", '%dd%mm%YY')) = extract(year from CURRENT_DATE)