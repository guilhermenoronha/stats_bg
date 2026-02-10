{{ config(materialized='incremental', unique_key=['execution_date', 'name'], on_schema_change='sync_all_columns') }}

with

matches as (
	select 
		*, 
		(rank() over (partition by id order by score asc)) as inverse_rank 
	from {{ ref('matches') }} 
),
games as (select * from {{ ref('games') }}),
bg_mechanics as (select * from {{ ref('bg_mechanics') }}),
players as (select * from {{ ref('players') }}),
games_per_player as (select player, cast(count(game) as numeric) as total_games from {{ ref('games_per_player') }} group by player),
bg_owners as (select * from {{ ref('bg_owners') }}),
attendances as (select * from {{ ref('attendances') }}),


max_score_per_match as(
    select 
        m.id,
        m.game_name,
        g.weight,
        count(m.id) as players_qty,
        max(m.score) as winner_score
    from matches m
    left join games g on m.game_id = g.id 
    group by m.id, m.game_name, g.weight
),

cooperative_games as (
	select distinct 
        g.id, 
        g.name, 
        g.weight
	from games g 
	join bg_mechanics bm on g.id = bm.game_id
	where bm.mechanic_id = 20 or lower(g.name) like '%dungeons & dragons%'
),

competitive_games as (
	select id, name, weight from games
	except 
	select id, name, weight from cooperative_games
),

competitive_matches as (
	select 
        p.id, 
        count(1) as total_matches
	from matches m
	join competitive_games cg on m.game_id = cg.id
	left join players p on p.id = m.player_id
	group by p.id
),

base_rank as (
	select
		p.name,
		m.id,
		m.rank,
		m.inverse_rank,
		m.score,
		cp.total_matches
	from players p
	left join matches m on p.id = m.player_id
	join competitive_games g on g.id = m.game_id 
	left join competitive_matches cp on cp.id = p.id
	where cp.total_matches >= 10
),

opponents_rank as (
		select
			name,
			round(avg(inverse_rank - 1), 2) as opponent_rank
		from base_rank
		group by name
),

winners_rank as (
	select 
        br.name, 
        round(cast(count(score) as numeric)/max(total_matches) * 100, 2) as winner_rank	
	from base_rank br
	join max_score_per_match mspm on br.id = mspm.id and br.rank = 1
	group by br.name	
),

losers_rank as (
	select 
        br.name, 
        round(cast(count(score) as numeric)/max(total_matches) * 100, 2) as loser_rank	
	from base_rank br
	join max_score_per_match mspm on br.id = mspm.id and br.inverse_rank = 1
	group by br.name	
),

vices_rank as (
	select 
        br.name, 
        round(cast(count(score) as numeric)/max(total_matches) * 100, 2) as vice_rank
	from base_rank br
	join max_score_per_match mspm on br.id = mspm.id and br.rank = 2
	group by br.name	
),

weighted_player_score as (
	select 
        p.name, 
        g.weight * a.players_qty * (1/m.rank::float) as weighted_player_score,
        m.weighted_rank * a.players_qty as weighted_rank,
        m.id
	from players p
	left join matches m on p.id = m.player_id
	join competitive_games g on g.id = m.game_id 
	left join competitive_matches cp on cp.id = p.id
	join max_score_per_match a on m.id = a.id 
	where cp.total_matches >= 10 
),

weighted_rank as (
	select 
		name,
		(sum(weighted_rank)/count(id))::numeric as weighted_rank
	from weighted_player_score mw
	group by name
),

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

session_with_players_game_in_percentage as (
	select 
		swmg.name, 
		round((swmg.session_with_my_game / app.attendance_per_player::numeric) * 100, 2) as session_with_players_game_in_percentage
	from session_with_my_game swmg 
	left join attendances_per_player app on swmg.id = app.id
),


final as (
	select distinct
		p.name,
		coalesce(winner_rank, 0) as winner_rank,
		coalesce(loser_rank, 0) as loser_rank,
		coalesce(vice_rank, 0) as vice_rank,
		coalesce(weighted_rank, 0) as weighted_rank,
		coalesce(total_games, 0) as total_games,
		coalesce(session_with_players_game_in_percentage, 0) as session_with_players_game_in_percentage,
		coalesce(opponent_rank, 0) as opponent_rank,
		date(now()) as execution_date
	from players p
	left join weighted_rank wr on p.name = wr.name
	left join winners_rank owr on p.name = owr.name
	left join losers_rank lr on p.name = lr.name
	left join vices_rank vr on p.name = vr.name
	left join games_per_player gpp on wr.name = gpp.player
	left join session_with_players_game_in_percentage swpgp on p.name = swpgp.name
	left join opponents_rank opp on opp.name = p.name
)

select * from final