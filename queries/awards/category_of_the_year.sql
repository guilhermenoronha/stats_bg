-- CATEGORY OF THE YEAR
WITH DISTINCT_MATCHES AS (
	SELECT DISTINCT "ID", "GAME_ID" 
	FROM stats_bg.bronze."MATCHES"
)
SELECT C."NAME", COUNT(BC."CATEGORY_ID") AS TOTAL_PLAYED
FROM DISTINCT_MATCHES M
LEFT JOIN stats_bg.bronze."BG_CATEGORIES" BC ON M."GAME_ID" = BC."GAME_ID"
LEFT JOIN stats_bg.bronze."CATEGORIES" C ON CAST(C."ID" as INT) = BC."CATEGORY_ID"  
GROUP BY 1
ORDER BY 2 DESC