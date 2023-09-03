-- kpi meetings
select (cast(count(distinct A."DATE") as FLOAT)/(select extract(WEEK from CURRENT_DATE))/0.85) as kpi_meetings
from stats_bg.bronze."ATTENDANCES" a

-- kpi attendances
WITH PLAYERS_PER_SESSION AS(
SELECT M."DATE", COUNT(DISTINCT M."PLAYER_ID") AS PLAYERS_PER_SESSION
FROM stats_bg.bronze."MATCHES" M
GROUP BY 1
)
SELECT AVG(PLAYERS_PER_SESSION)/4 AS kpi_avg_person_per_session
FROM PLAYERS_PER_SESSION

-- hosts kpi
with last_8_meetings as (
select "PLAYER_ID" as hosts
from stats_bg.bronze."ATTENDANCES" a
where "IS_HOST"  
order by to_date(A."DATE", '%dd%mm%YY') desc
limit 8
)
select cast(count(distinct(hosts)) as FLOAT)/8 as kpi_hosts
from last_8_meetings