with 
attendances as (select * from {{ ref('attendances') }}),
games as (select distinct date, game_name from {{ ref('matches') }} order by 1),

grouped_players as (
	select 
		date, 
		array_agg(player_name) as grp,
		lag (array_agg(player_name), 1) over (order by date) as last_grp
	from attendances a group by 1 order by 1
),

players_minus_lag as(
select date, array_agg(diff) as diffed_group
from
(
  select date, unnest(grp)
  from grouped_players
  except
  select date, unnest(last_grp)
  from grouped_players
  order by 1
) t(date, diff)
group by date
order by date
),

lag_minus_players as(
    select date, array_agg(diff) as diffed_group
    from
    (
        select date, unnest(last_grp)
        from grouped_players
        except
        select date, unnest(grp)
        from grouped_players
        order by 1
    ) t(date, diff)
    group by 1
    order by 1
),

players as (
    select 
        gp.date, 
        coalesce(greatest(array_length(gl.diffed_group, 1), array_length(lg.diffed_group, 1)), 0) as interchanging_players
    from grouped_players gp
    left join players_minus_lag gl on gp.date = gl.date
    left join lag_minus_players lg on gp.date = lg.date
),

grouped_games as (
	select distinct
		date, 
		array_agg(game_name) as grp,
		lag(array_agg(game_name), 1) over (order by date) as last_grp
	from games a group by 1 order by 1
),

games_minus_lag as(
    select date, array_agg(diff) as diffed_group
    from
    (
        select date, unnest(grp)
        from grouped_games
        except
        select date, unnest(last_grp)
        from grouped_games
        order by 1
    ) t(date, diff)
    group by date
    order by date
),

lag_minus_games as(
    select date, array_agg(diff) as diffed_group
    from
    (
        select date, unnest(last_grp)
        from grouped_games
        except
        select date, unnest(grp)
        from grouped_games
        order by 1
    ) t(date, diff)
    group by date
    order by date
),

games_interchanging as (
    select 
        gp.date, 
        coalesce(greatest(array_length(gl.diffed_group, 1), array_length(lg.diffed_group, 1)), 0) as interchanging_games
    from grouped_games gp
    left join games_minus_lag gl on gp.date = gl.date
    left join lag_minus_games lg on gp.date = lg.date
),

hosts as (
	select distinct 
		date, 
		player_id
	from attendances 
	where is_host 
	order by 1
),

host_changed as (
	select 
		date,
		player_id,
		case when (player_id - lag(player_id, 1) over (order by date)) != 0 then true else false end as interchanging_hosts
	from hosts
),

final as (
    select 
        p.date,
        p.interchanging_players,
        g.interchanging_games,
        h.interchanging_hosts
    from players p
    join games_interchanging g on p.date = g.date
    join host_changed h on p.date = h.date
)

select * from final