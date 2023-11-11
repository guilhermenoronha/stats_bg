with

matches as (select * from {{ ref('matches') }}),
games as (select * from {{ ref('games') }}),
bg_mechanics as (select * from {{ ref('bg_mechanics') }}),
players as (select * from {{ ref('players') }}),


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

only_winners_rank as (
	select 
        p.name, 
        round(cast(count(score) as numeric)/max(total_matches) * 100, 2) as winners_rank
	from players p
	left join matches m on p.id = m.player_id
	join competitive_games g on g.id = m.game_id 
	left join competitive_matches cp on cp.id = p.id
	join max_score_per_match a on m.id = a.id and m.rank = 1
	where cp.total_matches >= 10
	group by p.name
),

weighted_player_score as (
	select 
        p.name, 
        g.weight * a.players_qty * (1/m.rank::float) as weighted_player_score,
        g.weight * a.players_qty as max_score,
        m.weighted_rank,
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

final as (
	select 
		wr.name,
		winners_rank,
		weighted_rank
	from weighted_rank wr
	join only_winners_rank owr on wr.name = owr.name
)

select * from final