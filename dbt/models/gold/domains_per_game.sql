with
    domains as (select * from {{ ref('domains') }}),
    bg_domains as (select * from {{ ref('bg_domains') }}),
    games as (select * from {{ ref('games') }}),

final as (
    select distinct 
        d."name" as domain,
        g."name" as game
    from domains d 
    left join bg_domains bd on d.id = bd.domain_id
    left join games g on bd.game_id = g.id
    where g.game_type = 'B'    
)

select * from final