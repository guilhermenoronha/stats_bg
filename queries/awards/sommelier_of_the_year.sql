-- SOMMELIER OF THE YEAR
SELECT P."NAME", COUNT(DISTINCT M."ID") AS TOTAL_MATCHES, COUNT(DISTINCT BO."GAME_ID") AS TOTAL_GAMES
FROM stats_bg.bronze."PLAYERS" P
LEFT JOIN stats_bg.bronze."BG_OWNERS" BO ON BO."USER_ID" = P."ID"
JOIN stats_bg.bronze."MATCHES" M ON M."GAME_ID" = BO."GAME_ID"
LEFT JOIN stats_bg.bronze."GAMES" G ON G."ID"  = BO."GAME_ID"
GROUP BY 1
ORDER BY 2 DESC