with
    matches as (select * from {{ ref('matches') }})

	,attendances as (
		select distinct 
			 m."date"
			,m.player_id 
			,m.player_name 
			,m.player_membership
			,m.host_name = m.player_name as is_host
		from matches m
	)

select * from attendances