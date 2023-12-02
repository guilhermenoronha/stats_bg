with 

matches as (select * from {{ ref('matches') }}),
players as (select * from {{ ref('players') }}),
bg_owners as (select * from {{ ref('bg_owners') }}),
attendances as (select * from {{ ref('attendances') }}),

session_with_my_game as (

	select
        p.id,
		p.name,
		count(distinct m.date) as session_with_my_game
	from matches m
	left join players p on m.player_id = p.id 
	join bg_owners bo on m.player_id = bo.user_id and m.game_id = bo.game_id 
	group by p.id, p.name
),

attendances_per_player as (
	select
        p.id,
		p.name,
		count(distinct a.date) as attendance_per_player
	from attendances a
	left join players p on a.player_id = p.id
	group by p.id, p.name
),

final as (
	select 
		swmg.name, 
		round((swmg.session_with_my_game / app.attendance_per_player::numeric) * 100, 2) as session_with_players_game_in_percentage
	from session_with_my_game swmg 
	left join attendances_per_player app on swmg.id = app.id
)

select * from final