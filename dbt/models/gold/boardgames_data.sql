{{
    config(
        materialized="table"
    )
}}

with
     games as (select * from {{ ref("games") }})
    ,bg_mechanics as (select * from {{ ref("bg_mechanics") }})
    ,mechanics as (select * from {{ ref("mechanics") }})
    ,bg_themes as (select * from {{ ref("bg_themes") }})
    ,themes as (select * from {{ ref("themes") }})
    ,bg_categories as (select * from {{ ref("bg_categories") }})
    ,categories as (select * from {{ ref("categories") }})
    ,bg_domains as (select * from {{ ref("bg_domains") }})
    ,domains as (select * from {{ ref("domains") }})
    ,bg_owners as (select * from {{ ref("bg_owners") }})
    ,players as (select * from {{ ref("players") }} where membership = 'M')

select 
	 g.name
    ,g.game_type
    ,g.ludopedia_url
    ,g.min_age
    ,g.min_players
    ,g.max_players
    ,g.lst_dt_played
    ,g.weight
    ,g.min_best_players
    ,g.max_best_players
    ,g.playing_time_real_min
	,string_agg(distinct replace(coalesce(c.name, 'Não encontrado'), ' / ', '/'), ', ') as categories
	,string_agg(distinct replace(coalesce(d.name, 'Não encontrado'), ' / ', '/'), ', ') as domains
	,string_agg(distinct replace(coalesce(m.name, 'Não encontrado'), ' / ', '/'), ', ') as mechanics
	,string_agg(distinct replace(coalesce(t.name, 'Não encontrado'), ' / ', '/'), ', ') as themes
	,string_agg(distinct p."name", ', ') as owners
from games g
left join bg_mechanics bm on g.id = bm.game_id
left join mechanics m on m.id = bm.mechanic_id
left join bg_themes bt on g.id = bt.game_id
left join themes t on t.id = bt.theme_id
left join bg_categories bc on g.id = bc.game_id
left join categories c on c.id = bc.category_id
left join bg_domains bd on g.id = bd.game_id
left join domains d on d.id = bd.domain_id
left join bg_owners bo on g.id = bo.game_id
left join players p on p.id = bo.user_id
group by g.name, g.game_type, g.ludopedia_url, g.min_age, g.min_players, g.max_players, g.lst_dt_played,
         g.weight, g.min_best_players, g.max_best_players, g.playing_time_real_min