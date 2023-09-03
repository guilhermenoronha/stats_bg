-- STRATEGIST OF THE YEAR
WITH
AGG_FILTER AS(
	SELECT 	M."ID", 
			MAX(M."SCORE") AS MAX_SCORE
	FROM stats_bg.bronze."MATCHES" M
	GROUP BY 1
),
COOPERATIVE_GAMES AS (
	SELECT DISTINCT G."ID", G."NAME", G."WEIGHT"  
	FROM stats_bg.bronze."GAMES" G 
	JOIN stats_bg.bronze."BG_MECHANICS" BM ON G."ID" = BM."GAME_ID" 
	WHERE CAST(BM."MECHANIC_ID" AS INT) = 20 OR G."NAME" LIKE '%Dungeons & Dragons%'
),
COMPETITIVE_GAMES AS (
	SELECT G."ID", G."NAME", G."WEIGHT" FROM stats_bg.bronze."GAMES" G 
	EXCEPT 
	SELECT CG."ID", CG."NAME", CG."WEIGHT" FROM COOPERATIVE_GAMES CG
),
COMPETITIVE_MATCHES AS (
	SELECT P."ID", COUNT(1) AS TOTAL_MATCHES
	FROM stats_bg.bronze."MATCHES" M
	JOIN COMPETITIVE_GAMES CG ON M."GAME_ID" = CG."ID"
	LEFT JOIN stats_bg.bronze."PLAYERS" P ON P."ID" = M."PLAYER_ID" 
	GROUP BY 1
),
MATCH_WINNERS AS (
	SELECT P."NAME", M."SCORE", P."ID", G."WEIGHT", CP.TOTAL_MATCHES
	FROM stats_bg.bronze."PLAYERS" P
	LEFT JOIN stats_bg.bronze."MATCHES" M ON P."ID" = M."PLAYER_ID"
	JOIN COMPETITIVE_GAMES G ON G."ID" = M."GAME_ID" 
	LEFT JOIN COMPETITIVE_MATCHES CP ON CP."ID" = P."ID"
	JOIN AGG_FILTER A ON M."ID" = A."ID" AND M."SCORE" = A."max_score"
	WHERE CP.TOTAL_MATCHES >= 10 
)
SELECT 
	"NAME", 
	ROUND(CAST(COUNT(MW."SCORE") AS NUMERIC)/MAX(TOTAL_MATCHES) * 100, 2) AS TOTAL_WINS
	FROM MATCH_WINNERS MW
	GROUP BY 1