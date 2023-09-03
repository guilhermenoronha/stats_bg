-- EXPLORER OF THE YEAR
SELECT P."NAME", COUNT(DISTINCT M."GAME_ID") AS DIFFERENT_GAMES_PLAYED
FROM stats_bg.bronze."PLAYERS" P
LEFT JOIN stats_bg.bronze."MATCHES" M ON P."ID" = M."PLAYER_ID"
GROUP BY 1
ORDER BY 2 DESC