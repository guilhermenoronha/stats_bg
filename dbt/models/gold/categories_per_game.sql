with
    categories as (select * from {{ ref('categories') }}),
    bg_categories as (select * from {{ ref('bg_categories') }}),
    games as (select * from {{ ref('games') }}),

final as (
    select 
        distinct c."name" as category,
        g."name" as game
    from categories c 
    left join bg_categories bc on c.id = bc.category_id
    left join games g on bc.game_id = g.id
    where g.game_type = 'B'
)

select * from final