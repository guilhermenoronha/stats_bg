with

themes as (select * from {{ ref('themes') }}),
bg_themes as (select * from {{ ref('bg_themes') }}),
games as (select * from {{ ref('games') }}),

final as(
    select distinct 
        t."name" as theme,
        g."name" as game
    from themes t 
    left join bg_themes bt on t.id = bt.theme_id 
    left join games g on bt.game_id = g.id
    where g.game_type = 'B' 
)

select * from final