WITH 

PLAYERS AS (SELECT * FROM {{ ref('players') }} ORDER BY name),
MATCHES AS (SELECT * FROM {{ ref('matches') }}),

only_members_matches AS (
	SELECT 
		 A."date"
		,A.id
		,A.player_id
	FROM matches A
	WHERE A.player_id in ( SELECT id FROM PLAYERS WHERE membership = 'M' )
),

only_guests_matches AS (
	SELECT 
		 A."date"
		,A.id
		,A.player_id
	FROM matches A
	WHERE A.player_id in ( SELECT id FROM PLAYERS WHERE membership = 'G' )
),

session_groups as (
	select
		 STRING_AGG(p.name, ', ' ORDER BY p.name) as group_name
		,m.date
		,m.id
	from only_members_matches m
	left join players p on m.player_id = p.id
	where m.id not in (select id from only_guests_matches)
	group by m.date, m.id
	
)

select distinct
	 group_name::varchar
	,date::date
from session_groups